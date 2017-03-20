# -*- coding: utf-8 -*-
import datetime
import json
import logging

import scrapy

from spiders import ManoloBaseSpider
from ..item_loaders import ManoloItemLoader
from ..items import ManoloItem
from ..utils import make_hash


class MujerSpider(ManoloBaseSpider):
    name = 'mujer'
    allowed_domains = ['app.mimp.gob.pe']

    base_url = 'http://app.mimp.gob.pe:8080/visitaweb/ListarVisitas.do'
    NUMBER_OF_ITEMS_PER_PAGE = 20

    def start_requests(self):
        """
        The peruvian website delivers all the records starting from the
        requested date to the present.

        So if you ask for records starting from date 2011-10-01, you will
        get all records from between 2011-10-01 and today. You just need to
        iterate over the pagination to scrape all the records.
        """
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        print("SCRAPING from: {}".format(d1))
        yield self.initial_request(d1)

    def initial_request(self, date):
        date_str = date.strftime('%d/%m/%Y')

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
        return "{}?fecha={}".format(self.base_url, date.strftime('%Y%m%d'))

    def after_post(self, response):
        # send requests based on pagination
        res = json.loads(response.body)
        total_records = res['total']

        logging.info('Found {} records to scrape'.format(total_records))
        pages = total_records / self.NUMBER_OF_ITEMS_PER_PAGE + 1

        logging.info('Found {} pages to scrape'.format(pages))

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
        data = json.loads(response.body)
        rows = data['rows']

        for row in rows:
            l = ManoloItemLoader(item=ManoloItem())

            item_date = row.get('fec_fecha', '')
            if item_date:
                item_date = self.get_date_item(item_date, '%d/%m/%Y')
            l.add_value('institution', 'min. mujer')
            l.add_value('date', item_date)
            l.add_value('full_name', row['txt_nombre_visitante'])
            l.add_value('id_number', row['txt_dni'])
            l.add_value('id_document', 'DNI')
            l.add_value('entity', row['txt_entidad'])
            l.add_value('reason', row['txt_observacion'])
            l.add_value('host_name', row['txt_nombre_funcionario'])
            l.add_value('office', row['txt_unidad'])
            l.add_value('time_start', row['ingreso'])
            l.add_value('time_end', row['salida'])

            item = l.load_item()

            item = make_hash(item)
            yield item
