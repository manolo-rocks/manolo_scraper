# -*- coding: utf-8 -*-
"""
Scraper for Ministerio de la Mujer
"""
import datetime
import json
import logging

import scrapy

from spiders import ManoloBaseSpider
from ..item_loaders import ManoloItemLoader
from ..items import ManoloItem
from ..utils import make_hash


# url: http://webapp.mimp.gob.pe:8080/visitaweb/
class MujerSpider(ManoloBaseSpider):
    name = 'mujer'
    allowed_domains = ['webapp.mimp.gob.pe']

    base_url = 'http://webapp.mimp.gob.pe:8080/visitaweb/ListarVisitas.do'
    NUMBER_OF_ITEMS_PER_PAGE = 20

    def initial_request(self, date):
        date_str = date.strftime("%d/%m/%Y")

        params = {
            'page': '1',
            'rows': str(self.NUMBER_OF_ITEMS_PER_PAGE)
        }

        url = self._get_url(date)

        return scrapy.FormRequest(url=url, formdata=params,
                                  meta={'date': date_str},
                                  dont_filter=True,
                                  callback=self.after_post)

    def _get_url(self, date):
        return "{}?fecha={}".format(self.base_url, datetime.date.strftime(date, '%Y%m%d'))

    def after_post(self, response):
        # send requests based on pagination
        res = json.loads(response.body)
        total_records = res['total']

        logging.info("Found {} records to scrape".format(total_records))
        pages = total_records / self.NUMBER_OF_ITEMS_PER_PAGE + 1

        logging.info("Found {} pages to scrape".format(pages))

        for page in range(pages):
            params = {
                'page': str(page + 1),
                'rows': str(self.NUMBER_OF_ITEMS_PER_PAGE)
            }

            yield scrapy.FormRequest(url=response.url, formdata=params,
                                     meta={
                                         'date': response.meta['date'],
                                     },
                                     dont_filter=True,
                                     callback=self.parse)

    def parse(self, response):

        date_obj = datetime.datetime.strptime(response.meta['date'], '%d/%m/%Y')
        date = datetime.datetime.strftime(date_obj, '%Y-%m-%d')

        data = json.loads(response.body)
        rows = data['rows']

        for row in rows:
            l = ManoloItemLoader(item=ManoloItem())

            l.add_value('institution', 'min. mujer')
            l.add_value('date', date)
            l.add_value('full_name', row['txt_visitante'])
            l.add_value('id_number', row['txt_dni'])
            l.add_value('id_document', 'DNI')
            l.add_value('entity', row['entidad'])
            l.add_value('reason', row['txt_observacion'])
            l.add_value('host_name', row['txt_nombre_funcionario'])
            l.add_value('office', row['txt_unidad'])
            l.add_value('time_start', row['ingreso'])
            l.add_value('time_end', row['salida'])

            item = l.load_item()

            item = make_hash(item)
            yield item
