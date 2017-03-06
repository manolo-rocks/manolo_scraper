# -*- coding: utf-8 -*-
import re

from scrapy import FormRequest, Request

from spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash


class MinsaSpider(ManoloBaseSpider):
    name = 'minsa'
    allowed_domains = ['appsalud.minsa.gob.pe']
    REQUEST_DATE_FORMAT = '%d/%m/%Y'
    MORE_PAGES_SYMBOL = '...'
    NUMBER_OF_PAGE_REGEX = r'Page\$(\w+)'

    def initial_request(self, date):
        date_str = date.strftime(self.REQUEST_DATE_FORMAT)

        request = Request(
            url="http://appsalud.minsa.gob.pe/regvisitascons/listado.aspx",
            dont_filter=True,
            callback=self.parse_initial_request,
        )
        request.meta['date'] = date_str
        return request

    def parse_initial_request(self, response):
        date_str = response.meta['date']
        request = FormRequest.from_response(
            response,
            formdata={
                'txtFecha': date_str,
                'txtFechaF': date_str,
                'btnListar': 'Listar',
                'DDLFuncionario': '',
            },
            dont_filter=True,
            dont_click=True,
            callback=self.parse_pages,
        )
        request.meta['date'] = date_str
        yield request

    def parse_pages(self, response):
        page_offset = response.meta.get('page_offset', 2)
        date_str = response.meta['date']

        # Parse Items
        items = self.parse(response)
        for item in items:
            yield item

        rows = response.xpath('//table[@id="DTGVisitas"]/tr')
        pagination_links = rows.xpath('td/font/table//td/font/a')

        if pagination_links:
            last_page_href = pagination_links.xpath('./@href').extract()[-1]
            last_page_link_text = pagination_links.xpath('./font/text()').extract()[-1]
            is_there_pages = re.search(self.NUMBER_OF_PAGE_REGEX, last_page_href)

            if is_there_pages:
                last_page = int(is_there_pages.group(1))
                pages_limit = last_page + 1

                # Is there more pages?
                if last_page_link_text == self.MORE_PAGES_SYMBOL:
                    pages_limit = last_page
                    request = self._request_page(response, last_page, date_str, self.parse_pages)
                    request.meta['page_offset'] = last_page + 1
                    yield request

                for page in range(page_offset, pages_limit):
                    request = self._request_page(response, page, date_str, self.parse)
                    yield request

    def _request_page(self, response, page_number, date_str, callback):
        request = FormRequest.from_response(
            response,
            formdata={
                'txtFecha': date_str,
                'txtFechaF': date_str,
                'DDLFuncionario': '',
                '__EVENTTARGET': 'DTGVisitas',
                '__EVENTARGUMENT': 'Page${}'.format(page_number),
            },
            dont_filter=True,
            dont_click=True,
            callback=callback,
        )

        request.meta['date'] = date_str
        return request

    def parse(self, response):
        rows = response.xpath('//table[@id="DTGVisitas"]/tr')

        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        for row in rows:
            data = row.xpath('td')
            if len(data) > 9:
                l = ManoloItemLoader(item=ManoloItem(), selector=row)

                l.add_value('institution', 'minsa')
                l.add_value('date', date)

                l.add_xpath('full_name', './td[3]/text()')
                l.add_xpath('id_document', './td[4]/text()')
                l.add_xpath('id_number', './td[5]/text()')
                l.add_xpath('entity', './td[6]/text()')
                l.add_xpath('reason', './td[7]/text()')
                l.add_xpath('host_name', './td[8]/text()')
                l.add_xpath('office', './td[9]/text()')
                l.add_xpath('title', './td[10]/text()')
                l.add_xpath('time_start', './td[11]/text()')
                l.add_xpath('time_end', './td[12]/text()')

                item = l.load_item()
                item = make_hash(item)
                yield item
