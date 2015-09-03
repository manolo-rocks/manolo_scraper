# -*- coding: utf-8 -*-
import re
import math

from scrapy import FormRequest, Request

from spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash


class CongresoSpider(ManoloBaseSpider):
    name = 'congreso'
    allowed_domains = ['regvisitas.congreso.gob.pe']
    NUMBER_OF_PAGES_PER_PAGE = 10

    def initial_request(self, date):
        date_str = date.strftime("%d/%m/%Y")

        # This initial request always hits the current page of the date.
        request = Request(url='http://regvisitas.congreso.gob.pe/regvisitastransparencia/',
                          meta={
                              'date': date_str,
                          },
                          dont_filter=True,
                          callback=self.parse_initial_request)

        return request

    def parse_initial_request(self, response):
        date = response.meta['date']
        request = self._request_initial_date_page(response, date, self.parse_pages)
        yield request

    def _request_initial_date_page(self, response, date_str, callback):
        formdata = {
            'TxtFecha': date_str,
            'BtnBuscar': 'Buscar'
        }

        request = FormRequest.from_response(response,
                                            formdata=formdata,
                                            dont_click=True,
                                            dont_filter=True,
                                            callback=callback
                                            )

        request.meta['date'] = date_str
        request.meta['current_page'] = 1
        return request

    def parse_pages(self, response):
        date = response.meta['date']

        # Parse Items
        items = self.parse(response)
        for item in items:
            yield item

        request = self._request_next_page(response, date, self.parse_pages)

        yield request

    def parse(self, response):
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        for row in response.xpath('//table[@class="grid"]/tr'):
            data = row.xpath('td')

            if len(data) > 9:
                full_name = data[2].xpath('./span/text()').extract_first(default='')

                if full_name.strip():
                    l = ManoloItemLoader(item=ManoloItem(), selector=row)
                    l.add_value('institution', 'congreso')
                    l.add_value('date', date)
                    l.add_value('full_name', full_name)

                    l.add_xpath('time_start', './td[2]/span/text()')
                    l.add_xpath('id_document', './td[4]/span/text()')
                    l.add_xpath('id_number', './td[5]/span/text()')
                    l.add_xpath('entity', './td[6]/span/text()')
                    l.add_xpath('reason', './td[7]/span/text()')
                    l.add_xpath('host_name', './td[8]/span/text()')
                    l.add_xpath('title', './td[9]/span/text()')
                    l.add_xpath('office', './td[10]/span/text()')
                    l.add_xpath('time_end', './td[11]/span/text()')

                    item = l.load_item()

                    item = make_hash(item)

                    yield item

    def _request_next_page(self, response, date_str, callback):
        current_page = int(response.meta['current_page'])

        total_string = response.css('#LblTotal').xpath('./text()').extract_first(default='')

        total = re.search(r'(\d+)', total_string)

        if total:
            # Deal with the next page.
            total = total.group(1)
            number_of_pages = self._get_number_of_pages(int(total))

            if current_page < number_of_pages:
                current_page += 1

                formdata = {
                    'TxtFecha': date_str,
                    'BtnBuscar': 'Buscar',
                    'LwVisitasCR$DpVisitasCR$ctl02$ctl00.x': '1',
                    'LwVisitasCR$DpVisitasCR$ctl02$ctl00.y': '1'
                }

                request = FormRequest.from_response(response,
                                                    formdata=formdata,
                                                    dont_click=True,
                                                    dont_filter=True,
                                                    callback=callback,
                                                    )

                request.meta['date'] = date_str
                request.meta['current_page'] = current_page

                return request

    def _get_number_of_pages(self, total_of_records):
        return int(math.ceil(total_of_records / float(self.NUMBER_OF_PAGES_PER_PAGE)))
