# -*- coding: utf-8 -*-
from scrapy import FormRequest, Request

from spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash


class AmbienteSpider(ManoloBaseSpider):
    name = 'ambiente'
    allowed_domains = ['visitas.minam.gob.pe']
    NUMBER_OF_PAGES_PER_PAGE = 10
    DATE_REQUEST_FORMAT = '%d/%m/%Y'

    def initial_request(self, date):
        date_str = date.strftime(self.DATE_REQUEST_FORMAT)

        # This initial request always hit the current page of the date.
        request = Request(url='http://visitas.minam.gob.pe/frmConsulta.aspx',
                          meta={
                              'date': date_str,
                          },
                          dont_filter=True,
                          callback=self.parse_initial_request)

        request.meta['date'] = date_str

        return request

    def parse_initial_request(self, response):
        date = response.meta['date']
        request = FormRequest.from_response(
            response,
            formdata={
                'txtDesde': date,
                'btnBuscar.x': '62',
                'btnBuscar.y': '15',
            },
            dont_filter=True,
            callback=self.parse_page,
        )

        request.meta['date'] = date

        yield request

    def parse_page(self, response):
        date = response.meta['date']

        pages = response.xpath('//table[@id="gvwConsulta"]//tr[@class="rgPager"]//table/tr/td')

        number_of_pages = len(pages)

        items = self.parse(response)

        # Parse items from the first page
        for item in items:
            yield item

        for page in range(2, number_of_pages + 1):
            request = self._get_page_request(response, page, date)
            yield request

    def parse(self, response):
        date = self.get_date_item(response.meta['date'], self.DATE_REQUEST_FORMAT)

        rows = response.xpath('//table[@id="gvwConsulta"]/tr[@class="rgRow" or @class="rgAltRow"]')

        for row in rows:
            l = ManoloItemLoader(item=ManoloItem(), selector=row)
            l.add_value('institution', 'ambiente')
            l.add_value('date', date)
            l.add_value('id_document', 'DNI')

            l.add_xpath('full_name', './/td[2]/text()')
            l.add_xpath('id_number', './/td[3]/text()')
            l.add_xpath('entity', './/td[4]/text()')
            l.add_xpath('reason', './/td[5]/text()')
            l.add_xpath('host_name', './/td[6]/text()')
            l.add_xpath('office', './/td[7]/text()')
            l.add_xpath('meeting_place', './/td[8]/text()')

            l.add_xpath('time_start', './/td[9]/text()')
            l.add_xpath('time_end', './/td[10]/text()')

            time_start = l.get_output_value('time_start')
            time_end = l.get_output_value('time_end')

            l.replace_value('time_start', self._get_time(time_start))
            l.replace_value('time_end', self._get_time(time_end))

            item = l.load_item()

            item = make_hash(item)

            yield item

    def _get_page_request(self, response, page, date):
        request = FormRequest.from_response(
            response,
            formdata={
                'txtDesde': date,
                '__EVENTTARGET': 'gvwConsulta',
                '__EVENTARGUMENT': 'Page${}'.format(page),
            },
            dont_filter=True,
            callback=self.parse,
        )
        request.meta['date'] = date
        return request

    # date_string: '28/08/2015 05:11:38 p.m.'
    def _get_time(self, date_string):
        if date_string is not None:
            date = date_string.split(' ')
            return date[1] + ' ' + date[2]

        return None
