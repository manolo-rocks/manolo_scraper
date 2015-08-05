# -*- coding: utf-8 -*-
import datetime
from datetime import date
from datetime import timedelta
import logging
import re

import scrapy
from scrapy import exceptions

from manolo_scraper.items import ManoloItem
from manolo_scraper.utils import make_hash


# SIstema de REgistro de VIsitas
class SireviSpider(scrapy.Spider):

    ajax_page_pattern = '/index.php?r=consultas/visitaConsulta/updateVisitasConsultaResultGrid&ajax=lst-visitas-consulta-result-grid&lstVisitasResult_page=%s'

    def __init__(self, date_start=None, *args, **kwargs):
        super(SireviSpider, self).__init__(*args, **kwargs)
        self.date_start = date_start

        if self.date_start is None:
            raise exceptions.UsageError('Enter start date as spider argument: -a date_start=')

        if self.institution_name is None:
            raise exceptions.UsageError('Enter a institution_name.')

    def start_requests(self):
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        d2 = date.today()
        # range to fetch
        delta = d2 - d1

        for i in range(delta.days + 1):
            my_date = d1 + timedelta(days=i)
            my_date_str = my_date.strftime("%d/%m/%Y")

            print("SCRAPING: {}".format(my_date_str))

            params = {
                'VisitaConsultaQueryForm[feConsulta]': my_date_str,
                'yt0': 'Consultar',
            }

            ajax_url = self.base_url + self.ajax_page_pattern % 1

            yield scrapy.FormRequest(url=ajax_url, formdata=params,
                                     meta={'date': my_date_str},
                                     dont_filter=True,
                                     callback=self.after_post)

    def after_post(self, response):
        page_links = response.css("li.last").xpath("./a/@href").extract()
        number_of_pages = re.findall(r'lstVisitasResult_page=(\d+)', str(page_links))

        try:
            number_of_pages = int(number_of_pages[0])
        except IndexError:
            number_of_pages = 1
        except TypeError:
            number_of_pages = 1

        params = {
            'VisitaConsultaQueryForm[feConsulta]': response.meta['date'],
            'yt0': 'Consultar',
        }

        for page_number in range(1, number_of_pages + 1):
            page_url = self.base_url + self.ajax_page_pattern % page_number

            yield scrapy.FormRequest(url=page_url, formdata=params,
                                     meta={'date': response.meta['date']},
                                     dont_filter=True,
                                     callback=self.parse)

    def parse(self, response):
        logging.info("PARSED URL {}".format(response.url))

        this_date_obj = datetime.datetime.strptime(response.meta['date'], '%d/%m/%Y')
        this_date_str = datetime.datetime.strftime(this_date_obj, '%Y-%m-%d')

        item = ManoloItem()
        item['full_name'] = ''
        item['entity'] = ''
        item['meeting_place'] = ''
        item['office'] = ''
        item['host_name'] = ''
        item['reason'] = ''
        item['institution'] = self.institution_name
        item['location'] = ''
        item['id_number'] = ''
        item['id_document'] = ''
        item['date'] = this_date_str
        item['title'] = ''
        item['time_start'] = ''
        item['time_end'] = ''

        selectors = response.xpath("//tr")

        for sel in selectors:
            fields = sel.xpath('.//td/text()').extract()

            if len(fields) > 3:
                # full name of visitor
                full_name = re.sub('\s+', ' ', fields[1])
                item['full_name'] = full_name.strip()

                item['entity'] = re.sub("\s+", " ", fields[3]).strip()
                item['reason'] = re.sub("\s+", " ", fields[4]).strip()
                item['host_name'] = re.sub("\s+", " ", fields[5]).strip()

                item['title'] = re.sub("\s+", " ", fields[6]).strip()
                item['office'] = re.sub("\s+", " ", fields[7]).strip()
                item['time_start'] = re.sub("\s+", " ", fields[8]).strip()

                try:
                    document_identity = fields[2].strip()
                except IndexError:
                    document_identity = ''

                if document_identity != '':
                    item['id_document'], item['id_number'] = self.get_dni(document_identity)

                try:
                    item['time_end'] = re.sub("\s+", " ", fields[9]).strip()
                except IndexError:
                    item['time_end'] = ''

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
