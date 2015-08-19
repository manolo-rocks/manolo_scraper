# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta

import re
import math

import scrapy

from spiders import ManoloBaseSpider

from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash, get_dni

# url: http://intranet.minem.gob.pe/GESTION/visitas_pcm


class MinemSpider(ManoloBaseSpider):
    name = 'minem'
    allowed_domains = ['http://intranet.minem.gob.pe']

    NUMBER_OF_PAGES_PER_PAGE = 20

    def start_requests(self):
        """
        Get starting date to scrape from our database

        :return: set of URLs
        """
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        d2 = datetime.datetime.strptime(self.date_end, '%Y-%m-%d').date()
        # range to fetch
        delta = d2 - d1

        for i in range(delta.days + 1):
            my_date = d1 + timedelta(days=i)
            my_date_str = my_date.strftime("%d/%m/%Y")
            print("SCRAPING: %s" % my_date_str)

            request = self.make_form_request(my_date_str, self.parse_pages, 1)

            yield request

    def parse_pages(self, response):
        total_of_records = response.css('#HID_CantidadRegistros').xpath('./@value').extract()

        try:
            total_of_records = int(total_of_records[0])
        except IndexError:
            total_of_records = 1
        except TypeError:
            total_of_records = 1

        number_of_pages = self.get_number_of_pages(total_of_records)

        for page in range(1, number_of_pages + 1):
            request = self.make_form_request(response.meta['date'], self.parse, page)
            yield request

    def parse(self, response):
        date_obj = datetime.datetime.strptime(response.meta['date'], '%d/%m/%Y')
        date = datetime.datetime.strftime(date_obj, '%Y-%m-%d')

        rows = response.xpath("//tr")

        for row in rows:
            l = ManoloItemLoader(item=ManoloItem(), selector=row)

            l.add_value('institution', 'minem')
            l.add_value('date', date)

            l.add_xpath('full_name', './td[3]/center/text()')
            l.add_xpath('entity', './td[5]/center/text()')
            l.add_xpath('reason', './td[6]/center/text()')
            l.add_xpath('host_name', './td[7]/center/text()')
            l.add_xpath('office', './td[8]/center/text()')
            l.add_xpath('meeting_place', './td[9]/center/text()')
            l.add_xpath('time_start', './td[10]/center/text()')
            l.add_xpath('time_end', './td[11]/center/text()')

            document_identity = row.xpath('td[4]/center/text()').extract_first(default='')

            id_document, id_number = get_dni(document_identity)

            l.add_value('id_document', id_document)
            l.add_value('id_number', id_number)

            item = l.load_item()

            item = make_hash(item)

            yield item

    def get_number_of_pages(self, total_of_records):
        return int(math.ceil(total_of_records / float(self.NUMBER_OF_PAGES_PER_PAGE)))

    def make_form_request(self, date_str, callback, page_number):
        page_url = 'http://intranet.minem.gob.pe/GESTION/visitas_pcm/Busqueda/DMET_html_SelectMaestraBuscador'

        start_from_record = self.NUMBER_OF_PAGES_PER_PAGE * (page_number - 1) + 1

        params = {
            'TXT_FechaVisita_Inicio': date_str,
            'Ls_Pagina': str(start_from_record),
            'Li_ResultadoPorPagina': '20',
            'FlgBuscador': '1',
            'Ls_ParametrosBuscador': 'TXT_FechaVisita_Inicio=10/08/2015|Ls_Pagina={}'.format(str(start_from_record)),
            }

        request = scrapy.FormRequest(url=page_url, formdata=params,
                                     meta={'date': date_str},
                                     dont_filter=True,
                                     callback=callback)
        return request
