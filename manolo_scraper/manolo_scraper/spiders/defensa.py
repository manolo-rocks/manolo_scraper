# -*- coding: utf-8 -*-
import datetime
import logging

import scrapy

from spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash, get_dni


class DefensaSpider(ManoloBaseSpider):
    name = 'defensa'
    allowed_domains = ['mindef.gob.pe']

    def start_requests(self):
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        d2 = datetime.datetime.strptime(self.date_end, '%Y-%m-%d').date()
        delta = d2 - d1

        for i in range(delta.days + 1):
            date = d1 + datetime.timedelta(days=i)
            date_str = date.strftime("%d/%m/%Y")
            logging.info("SCRAPING: {}".format(date_str))

            params = {'fechaqry': date_str}
            yield scrapy.FormRequest(url="http://www.mindef.gob.pe/visitas/qryvisitas.php", formdata=params,
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
        logging.info("PARSED URL {}".format(response.url))

        date_obj = datetime.datetime.strptime(response.meta['date'], '%d/%m/%Y')
        date = datetime.datetime.strftime(date_obj, '%Y-%m-%d')

        item = ManoloItem()
        item['full_name'] = ''
        item['entity'] = ''
        item['meeting_place'] = ''
        item['office'] = ''
        item['host_name'] = ''
        item['reason'] = ''
        item['institution'] = 'defensa'
        item['location'] = ''
        item['id_number'] = ''
        item['id_document'] = ''
        item['date'] = date
        item['title'] = ''
        item['time_start'] = ''
        item['time_end'] = ''

        sels = response.xpath('//tr')
        for sel in sels:
            fields = sel.xpath('.//td[@class="clsdetalle"]')
            if len(fields) == 8:
                item['full_name'] = fields[1].xpath('text()').extract_first().strip()
                item['entity'] = fields[3].xpath('text()').extract_first().strip()
                item['host_name'] = fields[5].xpath('text()').extract_first().strip()
                item['reason'] = fields[4].xpath('text()').extract_first().strip()
                item['id_document'], item['id_number'] = get_dni(fields[2].xpath('text()').extract_first().strip())
                item['time_start'] = fields[6].xpath('text()').extract_first().strip()
                item['time_end'] = fields[7].xpath('text()').extract_first().strip()
                item = make_hash(item)
                yield item
