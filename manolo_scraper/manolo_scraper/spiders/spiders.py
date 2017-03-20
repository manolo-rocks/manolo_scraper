# -*- coding: utf-8 -*-
import datetime
import logging
import re
from exceptions import NotImplementedError

import scrapy
from scrapy import exceptions

from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash, get_dni


class ManoloBaseSpider(scrapy.Spider):

    def __init__(self, date_start=None, date_end=None, *args, **kwargs):
        super(ManoloBaseSpider, self).__init__(*args, **kwargs)

        self.date_start = date_start
        self.date_end = date_end

        today = datetime.date.today()

        if self.date_start is None:
            date_start = today - datetime.timedelta(days=14)
            self.date_start = date_start.strftime('%Y-%m-%d')

        if self.date_end is None:
            self.date_end = today.strftime('%Y-%m-%d')

        if self.days_between_dates(self.date_start, self.date_end) < 0:
            raise exceptions.UsageError("date_start must be less or equal to date_end")

    @staticmethod
    def days_between_dates(date_start, date_end):
        d1 = datetime.datetime.strptime(date_start, '%Y-%m-%d').date()
        d2 = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()
        delta = d2 - d1
        return delta.days

    def start_requests(self):
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        d2 = datetime.datetime.strptime(self.date_end, '%Y-%m-%d').date()
        # range to fetch
        delta = d2 - d1

        for day in range(delta.days + 1):
            date_obj = d1 + datetime.timedelta(days=day)
            print("SCRAPING: {}".format(date_obj))

            yield self.initial_request(date_obj)

    # Check if instance of requests
    def initial_request(self, date_obj):
        raise NotImplementedError

    @staticmethod
    def get_date_item(date_str, format):
        date_obj = datetime.datetime.strptime(date_str, format)
        return date_obj.strftime('%Y-%m-%d')


# SIstema de REgistro de VIsitas
class SireviSpider(ManoloBaseSpider):

    ajax_page_pattern = '/index.php?r=consultas/visitaConsulta/updateVisitasConsultaResultGrid&ajax=lst-visitas-consulta-result-grid&lstVisitasResult_page=%s'

    def __init__(self, *args, **kwargs):
        super(SireviSpider, self).__init__(*args, **kwargs)

        if self.institution_name is None:
            raise exceptions.UsageError('Enter a institution_name.')

    def initial_request(self, date):
        date_str = date.strftime("%d/%m/%Y")
        return self._request_page(date_str, 1, self.after_post)

    def after_post(self, response):
        page_links = response.css('li.last').xpath('./a/@href').extract_first(default='')
        is_number_of_pages = re.search(r'lstVisitasResult_page=(\d+)', page_links)
        number_of_pages = 1

        if is_number_of_pages:
            number_of_pages = int(is_number_of_pages.group(1))

        for page_number in range(1, number_of_pages + 1):
            yield self._request_page(response.meta['date'], page_number, self.parse)

    def _request_page(self, date_str, page_number, callback):
        params = {
            'VisitaConsultaQueryForm[feConsulta]': date_str,
            'yt0': 'Consultar',
        }

        page_url = self._get_page_url(page_number)

        return scrapy.FormRequest(url=page_url,
                                  formdata=params,
                                  meta={'date': date_str},
                                  dont_filter=True,
                                  callback=callback)

    def _get_page_url(self, page_number):
        return self.base_url + self.ajax_page_pattern % page_number

    def parse(self, response):
        logging.info("PARSED URL {}".format(response.url))

        date_str = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        rows = response.xpath("//tr")

        for row in rows:
            data = row.xpath('.//td').extract()

            if len(data) > 3:
                item = self.get_item(data, date_str, row)

                item = make_hash(item)

                yield item

    def get_item(self, data, date_str, row):
        l = ManoloItemLoader(item=ManoloItem(), selector=row)

        l.add_value('institution', self.institution_name)
        l.add_value('date', date_str)
        l.add_xpath('full_name', './td[2]/text()')
        l.add_xpath('entity', './td[4]/text()')
        l.add_xpath('reason', './td[5]/text()')
        l.add_xpath('host_name', './td[6]/text()')
        l.add_xpath('title', './td[7]/text()')
        l.add_xpath('office', './td[8]/text()')
        l.add_xpath('time_start', './td[9]/text()')
        l.add_xpath('time_end', './td[10]/text()')

        try:
            document_identity = data[2].strip()
        except IndexError:
            document_identity = ''

        if document_identity != '':
            id_document, id_number = get_dni(document_identity)

            l.add_value('id_document', id_document)
            l.add_value('id_number', id_number)

        return l.load_item()
