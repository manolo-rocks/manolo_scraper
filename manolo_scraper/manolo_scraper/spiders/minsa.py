import datetime
from datetime import timedelta

import re

from scrapy import FormRequest, Request

from spiders import ManoloBaseSpider
from ..items import ManoloItem

from ..utils import make_hash


class MinsaSpider(ManoloBaseSpider):
    name = 'minsa'
    allowed_domains = ['intranet5.minsa.gob.pe']
    REQUEST_DATE_FORMAT = '%d/%-m/%Y'
    MORE_PAGES_SYMBOL = '...'
    NUMBER_OF_PAGE_REGEX = r'Page\$(\w+)'

    def start_requests(self):
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        d2 = datetime.date.today()
        delta = d2 - d1

        for i in range(delta.days + 1):
            date = d1 + timedelta(days=i)
            date_str = date.strftime(self.REQUEST_DATE_FORMAT)
            print("SCRAPING: %s" % date_str)

            request = Request(url='http://intranet5.minsa.gob.pe/RegVisitasCons/listado.aspx',
                              dont_filter=True,
                              callback=self.parse_initial_request,
            )

            request.meta['date'] = date_str

            yield request

    def parse_initial_request(self, response):
        date_str = response.meta['date']

        request = FormRequest.from_response(response,
                                            formdata={
                                                'txtFecha': date_str,
                                                'txtFechaF': date_str,
                                                'btnListar': 'Listar',
                                                'DDLFuncionario': '[ -- Seleccione Funcionario o Empleado -- ]',
                                            },
                                            dont_filter=True,
                                            dont_click=True,
                                            callback=self.parse_pages
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

    def parse(self, response):
        rows = response.xpath('//table[@id="DTGVisitas"]/tr')

        date_obj = datetime.datetime.strptime(response.meta['date'], '%d/%m/%Y')

        for row in rows:
            data = row.xpath('td')
            if len(data) > 9:
                item = ManoloItem()

                item['full_name'] = ''
                item['id_document'] = ''
                item['id_number'] = ''
                item['institution'] = 'minsa'
                item['entity'] = ''
                item['reason'] = ''
                item['host_name'] = ''
                item['title'] = ''
                item['office'] = ''
                item['time_start'] = ''
                item['time_end'] = ''
                item['date'] = date_obj

                try:
                    item['full_name'] = data[2].xpath('./font/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['id_document'] = data[3].xpath('./font/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['id_number'] = data[4].xpath('./font/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['entity'] = data[5].xpath('./font/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['reason'] = data[6].xpath('./font/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['host_name'] = data[7].xpath('./font/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['office'] = data[8].xpath('./font/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['title'] = data[9].xpath('./font/text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['time_start'] = data[10].xpath('./font/text()').extract()[0].strip()
                except IndexError:
                    pass

                try:
                    item['time_end'] = data[11].xpath('./font/text()').extract()[0].strip()
                except IndexError:
                    pass

                item = make_hash(item)

                yield item

    def _request_page(self, response, page_number, date_str, callback):
        request = FormRequest.from_response(response,
                                            formdata={
                                                'txtFecha': date_str,
                                                'txtFechaF': date_str,
                                                'DDLFuncionario': '[ -- Seleccione Funcionario o Empleado -- ]',
                                                '__EVENTTARGET': 'DTGVisitas',
                                                '__EVENTARGUMENT': 'Page${}'.format(page_number),
                                            },
                                            dont_filter=True,
                                            dont_click=True,
                                            callback=callback
        )

        request.meta['date'] = date_str
        return request
