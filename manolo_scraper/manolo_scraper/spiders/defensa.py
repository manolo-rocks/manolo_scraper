# -*- coding: utf-8 -*-
import datetime
import logging
import re

import scrapy
from scrapy import exceptions

from manolo_scraper.items import ManoloItem
from manolo_scraper.utils import make_hash

class DefensaSpider(scrapy.Spider):
    name = "defensa"
    allowed_domains = ["mindef.gob.pe"]

    def __init__(self, date_start=None, *args, **kwargs):
        super(DefensaSpider, self).__init__(*args, **kwargs)
        self.base_url = "http://www.mindef.gob.pe/visitas/qryvisitas.php"

        self.date_start = date_start
        if self.date_start is None:
            raise exceptions.UsageError('Enter start date as spider argument: -a date_start=')

    def start_requests(self):
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        d2 = datetime.date.today()
        delta = d2 - d1

        for i in range(delta.days + 1):
            my_date = d1 + datetime.timedelta(days=i)
            my_date_str = my_date.strftime("%d/%m/%Y")
            logging.info("SCRAPING: {}".format(my_date_str))

            params = {'fechaqry': my_date_str}
            yield scrapy.FormRequest(url=self.base_url, formdata=params,
                                     meta={'date': my_date_str},
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
        this_date_obj = datetime.datetime.strptime(response.meta['date'], '%d/%m/%Y')
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
        item['date'] = this_date_obj
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
                item['id_document'], item['id_number'] = self.get_dni(fields[2].xpath('text()').extract_first().strip())
                item['time_start'] = fields[6].xpath('text()').extract_first().strip()
                item['time_end'] = fields[7].xpath('text()').extract_first().strip()
                item = make_hash(item)
                yield item

    def get_dni(self, document_identity):
        id_document = ''
        id_number = ''

        document_identity = document_identity.replace(':', ' ')
        document_identity = re.sub('\s+', ' ', document_identity)
        document_identity = document_identity.strip()
        document_identity = re.sub('^', ' ', document_identity)

        res = re.search("(.*)\s(([A-Za-z0-9]+\W*)+)$", document_identity)
        if res:
            id_document = res.groups()[0].strip()
            id_number = res.groups()[1].strip()

        if id_document == '':
            id_document = 'DNI'

        return id_document, id_number
