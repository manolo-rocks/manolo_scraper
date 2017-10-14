# -*- coding: utf-8 -*-
import datetime

import scrapy

from spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash, get_dni


class DefensaSpider(ManoloBaseSpider):
    name = 'defensa'
    allowed_domains = ['transparencia.gob.pe']
    base_url = 'http://200.37.34.66/visitas/visitas_transparencia.php'

    def initial_request(self, date):
        # There is no pagination in Defensa
        date_str = date.strftime("%d/%m/%Y")
        params = {'fecha': date_str}
        print("Params {}".format(params))
        return scrapy.FormRequest(
            url=self.base_url,
            formdata=params,
            meta={'date': date_str},
            dont_filter=True,
            callback=self.parse,
        )

    def start_requests(self):
        # Defensa returns all visits from starting date to present, no need
        # to iterate over each day
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()

        print("SCRAPING FROM: {} to present".format(d1))
        yield self.initial_request(d1)

    def parse(self, response):
        rows = response.xpath('//tr')
        for row in rows:
            data = row.xpath('.//td[@class="clsgriddata2"]')

            if len(data) > 5:
                l = ManoloItemLoader(item=ManoloItem(), selector=row)

                l.add_value('institution', 'defensa')
                l.add_xpath('date', './/td[2]/text()')

                l.add_xpath('full_name', './/td[3]/text()')
                l.add_xpath('entity', './/td[5]/text()')
                l.add_xpath('reason', './/td[6]/text()')
                l.add_xpath('host_name', './/td[7]/text()')
                l.add_xpath('title', './/td[8]/text()')
                l.add_xpath('office', './/td[9]/text()')
                l.add_xpath('time_start', './/td[10]/text()')
                l.add_xpath('time_end', './/td[11]/text()')

                id_document, id_number = get_dni(data[3].xpath('text()').extract_first(default=''))

                l.add_value('id_document', id_document)
                l.add_value('id_number', id_number)

                item = l.load_item()

                item = make_hash(item)

                yield item
