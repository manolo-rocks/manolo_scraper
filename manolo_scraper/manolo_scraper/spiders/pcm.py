# -*- coding: utf-8 -*-
import datetime
import logging
import re

import scrapy
from scrapy import exceptions

from manolo_scraper.items import ManoloItem
from manolo_scraper.utils import make_hash


class PcmSpider(scrapy.Spider):
    name = "pcm"
    allowed_domains = ["hera.pcm.gob.pe"]

    def __init__(self, date_start=None, *args, **kwargs):
        super(PcmSpider, self).__init__(*args, **kwargs)
        self.date_start = date_start
        self.base_url = "http://hera.pcm.gob.pe/Visitas/controlVisitas/index.php"

        if self.date_start is None:
            raise exceptions.UsageError('Enter start date as spider argument: -a date_start=')

    def start_requests(self):
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        d2 = datetime.date.today()
        # range to fetch
        delta = d2 - d1

        for i in range(delta.days + 1):
            my_date = d1 + datetime.timedelta(days=i)
            my_date_str = my_date.strftime("%d/%m/%Y")
            print("SCRAPING: %s" % my_date_str)

            params = {
                'r': 'consultas/visitaConsulta/index',
                'VisitaConsultaQueryForm[feConsulta]': my_date_str,
                'yt0': 'Consultar'
            }
            yield scrapy.FormRequest(url=self.base_url, formdata=params,
                                     meta={'date': my_date_str},
                                     dont_filter=True,
                                     callback=self.after_post)

    def after_post(self, response):
        total_count_records_string = response.xpath('//div[@class="summary"]/text()').extract_first()
        res = re.search('([0-9]+)\s+resultado', str(total_count_records_string))
        if res is not None:
            total_count_records = res.groups()[0]
            pages = int(total_count_records) / 15 + 1
            logging.info("Total pages {}".format(pages))

            for page in range(pages):
                args = [
                    'r=consultas/visitaConsulta/updateVisitasConsultaResultGrid',
                    'ajax=lst-visitas-consulta-result-grid',
                    'lstVisitasResult_page={}'.format(str(page + 1)),
                ]
                args = '&'.join(args)
                params = {
                    'VisitaConsultaQueryForm[feConsulta]': response.meta['date'],
                }
                url = "{}?{}".format(self.base_url, args)
                yield scrapy.FormRequest(url=url, formdata=params,
                                         meta={'date': response.meta['date']},
                                         dont_filter=True,
                                         callback=self.parse)

    def parse(self, response):
        logging.info("PARSED URL {}".format(response.url))
        item = ManoloItem()
        item['full_name'] = ''
        item['entity'] = ''
        item['meeting_place'] = ''
        item['office'] = ''
        item['host_name'] = ''
        item['reason'] = ''
        item['institution'] = 'pcm'
        item['location'] = ''
        item['id_number'] = ''
        item['id_document'] = 'DNI'
        item['title'] = ''
        item['time_start'] = ''
        item['time_end'] = ''

        rows = []
        rows += response.xpath('//tr[@class="odd"]')
        rows += response.xpath('//tr[@class="even"]')

        for row in rows:
            my_date_str = row.xpath('.//td[1]/text()').extract_first()
            item['date'] = datetime.datetime.strptime(my_date_str, '%d/%m/%Y').date()
            item['full_name'] = row.xpath('.//td[2]/text()').extract_first()
            item['id_document'], item['id_number'] = self.get_dni(row.xpath('.//td[3]/text()').extract_first())
            item['entity'] = row.xpath('.//td[4]/text()').extract_first()
            item['reason'] = row.xpath('.//td[5]/text()').extract_first()
            item['location'] = row.xpath('.//td[6]/text()').extract_first()
            item['host_name'] = row.xpath('.//td[7]/text()').extract_first()
            item['office'] = row.xpath('.//td[8]/text()').extract_first()
            item['meeting_place'] = row.xpath('.//td[9]/text()').extract_first()
            item['time_start'] = row.xpath('.//td[10]/text()').extract_first()
            item['time_end'] = row.xpath('.//td[11]/text()').extract_first()
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
