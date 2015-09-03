# -*- coding: utf-8 -*-
import scrapy

from spiders import ManoloBaseSpider
from ..item_loaders import ManoloItemLoader
from ..items import ManoloItem
from ..utils import make_hash


class ProduceSpider(ManoloBaseSpider):
    name = 'produce'
    allowed_domains = ['http://www2.produce.gob.pe']

    def initial_request(self, date):
        date_str = date.strftime("%d/%m/%Y")
        request = scrapy.FormRequest('http://www2.produce.gob.pe/produce/transparencia/visitas/',
                                     formdata={
                                         'desFecha': date_str,
                                         'desFechaF': date_str,
                                         'buscar': 'Consultar'
                                     },
                                     callback=self.parse)

        request.meta['date'] = date_str

        return request

    def parse(self, response):
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        rows = response.xpath('//table[@class="tabla-login" and @width="100%"]//tr')

        for row in rows:
            data = row.xpath('td[@valign="top"]')

            if len(data) > 9:
                l = ManoloItemLoader(item=ManoloItem(), selector=row)

                l.add_value('institution', 'produce')
                l.add_value('date', date)

                l.add_xpath('time_start', './td[3]/text()')
                l.add_xpath('full_name', './td[4]/text()')
                l.add_xpath('id_document', './td[5]/text()')
                l.add_xpath('id_number', './td[6]/text()')
                l.add_xpath('reason', './td[7]/text()')
                l.add_xpath('host_name', './td[8]/text()')
                l.add_xpath('office', './td[9]/text()')
                l.add_xpath('time_end', './td[10]/text()')

                item = l.load_item()

                item = make_hash(item)

                yield item
