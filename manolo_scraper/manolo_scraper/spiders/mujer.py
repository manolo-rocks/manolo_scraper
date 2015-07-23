# -*- coding: utf-8 -*-
"""
Scraper for Ministerio de la Mujer
"""
import datetime
import json
import logging
import re

import scrapy
from scrapy import exceptions

from manolo_scraper.items import ManoloItem
from manolo_scraper.utils import make_hash


class MujerSpider(scrapy.Spider):
    name = "mujer"
    allowed_domains = ["webapp.mimp.gob.pe"]

    def __init__(self, date_start=None, *args, **kwargs):
        super(MujerSpider, self).__init__(*args, **kwargs)
        self.base_url = "http://webapp.mimp.gob.pe:8080/visitaweb/ListarVisitas.do"

        self.date_start = date_start
        if self.date_start is None:
            raise exceptions.UsageError('Enter start date as spider argument: -a date_start=')

    def start_requests(self):
        """
        This webpage returns all items from requested date to present. So there
        is no need to loop and do requests for all dates from date_start to present.
        It is enough to do one request for the date_start.
        """
        my_date = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        my_date_str = my_date.strftime("%d/%m/%Y")
        logging.info("SCRAPING: {}".format(my_date_str))

        params = {'page': '1', 'rows': '20'}
        url = "{}?fecha={}".format(self.base_url, datetime.date.strftime(my_date, '%Y%m%d'))
        logging.info("URL to scrape {}".format(url))
        yield scrapy.FormRequest(url=url, formdata=params,
                                 meta={'date': my_date_str},
                                 dont_filter=True,
                                 callback=self.after_post)

    def after_post(self, response):
        # send requests based on pagination
        res = json.loads(response.body)
        total_records = res['total']
        logging.info("Found {} records to scrape".format(total_records))
        pages = total_records/20 + 1
        logging.info("Found {} pages to scrape".format(pages))

        for page in range(pages):
            params = {
                'page': str(page + 1),
                'rows': '20',
            }
            yield scrapy.FormRequest(url=response.url, formdata=params,
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
        item['institution'] = 'min. mujer'
        item['location'] = ''
        item['id_number'] = ''
        item['id_document'] = 'DNI'
        item['title'] = ''
        item['time_start'] = ''
        item['time_end'] = ''
        data = json.loads(response.body)
        rows = data['rows']
        for row in rows:
            item['date'] = datetime.datetime.strptime(row['txt_fecha'], '%d/%m/%Y')
            item['full_name'] = row['txt_visitante']
            item['id_number'] = row['txt_dni']
            item['entity'] = row['entidad']
            item['reason'] = row['txt_observacion']
            item['host_name'] = row['txt_nombre_funcionario']
            item['office'] = row['txt_unidad']
            item['time_start'] = row['ingreso']
            item['time_end'] = row['salida']
            item = make_hash(item)
            yield item
