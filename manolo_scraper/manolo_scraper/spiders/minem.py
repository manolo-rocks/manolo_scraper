# -*- coding: utf-8 -*-
import datetime
from datetime import date
from datetime import timedelta
import re
import math

import scrapy
from scrapy import exceptions

from ..items import ManoloItem
from ..utils import make_hash, get_dni


class MinemSpider(scrapy.Spider):
    name = "minem"
    allowed_domains = ["http://intranet.minem.gob.pe"]

    NUMBER_OF_PAGES_PER_PAGE = 20

    def __init__(self, date_start=None, *args, **kwargs):
        super(MinemSpider, self).__init__(*args, **kwargs)
        self.date_start = date_start
        if self.date_start is None:
            raise exceptions.UsageError('Enter start date as spider argument: -a date_start=')

    def start_requests(self):
        """
        Get starting date to scrape from our database

        :return: set of URLs
        """
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        d2 = date.today()
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

        item = ManoloItem()
        item['full_name'] = ''
        item['entity'] = ''
        item['meeting_place'] = ''
        item['office'] = ''
        item['host_name'] = ''
        item['reason'] = ''
        item['institution'] = 'minem'
        item['location'] = ''
        item['id_number'] = ''
        item['id_document'] = ''
        item['date'] = date_obj
        item['title'] = ''
        item['time_start'] = ''
        item['time_end'] = ''

        selectors = response.xpath("//tr")

        for sel in selectors:
            fields = sel.xpath("td/center")

            # full name of visitor
            full_name = fields[1].xpath("text()").extract()
            try:
                full_name = full_name[0]
            except IndexError:
                pass
            full_name = re.sub("\s+", " ", full_name)
            item['full_name'] = full_name.strip()

            item['entity'] = re.sub("\s+", " ", fields[3].xpath("text()").extract()[0].strip())
            item['host_name'] = re.sub("\s+", " ", fields[5].xpath("text()").extract()[0].strip())
            item['reason'] = re.sub("\s+", " ", fields[4].xpath("text()").extract()[0].strip())
            item['title'] = re.sub("\s+", " ", fields[6].xpath("text()").extract()[0].strip())
            item['office'] = re.sub("\s+", " ", fields[7].xpath("text()").extract()[0].strip())
            item['time_start'] = re.sub("\s+", " ", fields[8].xpath("text()").extract()[0].strip())

            try:
                document_identity = fields[2].xpath("text()").extract()[0].strip()
            except IndexError:
                document_identity = ''

            if document_identity != '':
                item['id_document'], item['id_number'] = get_dni(document_identity)

            try:
                item['time_end'] = re.sub("\s+", " ", fields[9].xpath("text()").extract()[0].strip())
            except IndexError:
                item['time_end'] = ''

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
