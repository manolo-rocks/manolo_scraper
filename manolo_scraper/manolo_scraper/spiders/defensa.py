# -*- coding: utf-8 -*-
import scrapy

from spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash, get_dni


class DefensaSpider(ManoloBaseSpider):
    name = 'defensa'
    allowed_domains = ['mindef.gob.pe']
    base_url = 'http://www.mindef.gob.pe/visitas/qryvisitas.php'

    def initial_request(self, date):
        date_str = date.strftime("%d/%m/%Y")

        params = {'fechaqry': date_str}

        return scrapy.FormRequest(url=self.base_url, formdata=params,
                                  meta={'date': date_str},
                                  dont_filter=True,
                                  callback=self.after_post)

    def after_post(self, response):
        # send requests based on pagination
        pages = response.xpath('//select[@id="pag_actual"]//option/text()').extract()
        for page in pages:
            params = {
                'fechaqry': response.meta['date'],
                'pag_actual': page,
            }
            yield scrapy.FormRequest(url=self.base_url, formdata=params,
                                     meta={'date': response.meta['date']},
                                     dont_filter=True,
                                     callback=self.parse)

    def parse(self, response):
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        rows = response.xpath('//tr')
        for row in rows:
            data = row.xpath('.//td[@class="clsdetalle"]')

            if len(data) == 8:
                l = ManoloItemLoader(item=ManoloItem(), selector=row)

                l.add_value('institution', 'defensa')
                l.add_value('date', date)

                l.add_xpath('full_name', './/td[@class="clsdetalle"][2]/text()')
                l.add_xpath('entity', './/td[@class="clsdetalle"][4]/text()')
                l.add_xpath('reason', './/td[@class="clsdetalle"][5]/text()')
                l.add_xpath('host_name', './/td[@class="clsdetalle"][6]/text()')
                l.add_xpath('time_start', './/td[@class="clsdetalle"][7]/text()')
                l.add_xpath('time_end', './/td[@class="clsdetalle"][8]/text()')

                id_document, id_number = get_dni(data[2].xpath('text()').extract_first(default=''))

                l.add_value('id_document', id_document)
                l.add_value('id_number', id_number)

                item = l.load_item()

                item = make_hash(item)

                yield item
