# -*- coding: utf-8 -*-
import scrapy

from spiders import ManoloBaseSpider
from ..item_loaders import ManoloItemLoader
from ..items import ManoloItem
from ..utils import make_hash


class INPESpider(ManoloBaseSpider):
    name = 'inpe'
    allowed_domains = [
        'www.peru.gob.pe',
        'visitasadm.inpe.gob.pe'
    ]

    def initial_request(self, date):
        date_str = date.strftime('%d/%m/%Y')
        request = scrapy.FormRequest('http://visitasadm.inpe.gob.pe/VisitasadmInpe/Controller',
                                     formdata={'vis_fec_ing': date_str},
                                     meta={'date': date_str},
                                     callback=self.parse,
                                     )

        return request

    def parse(self, response):
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        rows = response.xpath('//tr')

        for row in rows:
            data = row.xpath('td')

            if len(data) > 7:
                l = ManoloItemLoader(item=ManoloItem(), selector=row)

                l.add_value('institution', 'inpe')
                l.add_value('date', date)

                l.add_xpath('full_name', './td[3]/p/text()')
                l.add_xpath('id_document', './td[4]/p/text()')

                id_document = l.get_output_value('id_document')

                if id_document is None:
                    l.replace_value('id_document', 'Otros')

                l.add_xpath('id_number', './td[5]/p/text()')
                l.add_xpath('entity', './td[6]/p/text()')
                l.add_xpath('reason', './td[7]/p/text()')
                l.add_xpath('host_name', './td[8]/p/text()')

                # Add conditional, don't accept "---"
                l.add_xpath('title', './td[9]/p/text()')

                l.add_xpath('office', './td[10]/p/text()')

                l.add_xpath('time_start', './td[2]/text()')
                l.add_xpath('time_end', './td[11]/text()')

                item = l.load_item()

                item = make_hash(item)

                yield item
