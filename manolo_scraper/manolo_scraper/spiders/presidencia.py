# -*- coding: utf-8 -*-
from scrapy import Request

from spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash, get_dni


class PresidenciaSpider(ManoloBaseSpider):
    name = 'presidencia'
    allowed_domains = ['http://www.presidencia.gob.pe']
    base_url = 'http://www.presidencia.gob.pe/visitas'
    NUMBER_OF_ITEMS_PER_PAGE = 12

    def initial_request(self, date):
        date_str = date.strftime('%d/%m/%Y')

        request = self._request_page(date_str, 1, self.parse_initial_request)

        return request

    def _request_page(self, date_str, page, callback):
        offset = self.NUMBER_OF_ITEMS_PER_PAGE * (page - 1)

        url = self.base_url + '/consulta_visitas.php?fecha={}&pagina={}'.format(date_str, offset)

        request = Request(url=url,
                          meta={
                              'date': date_str,
                          },
                          dont_filter=True,
                          callback=callback)

        request.meta['date'] = date_str

        return request

    def parse_initial_request(self, response):
        date_str = response.meta['date']

        number_of_pages = int(response.xpath('//td[@class="textocampo2"]/b//option/text()').extract()[-1])

        if number_of_pages > 0:
            for page in range(1, number_of_pages + 1):
                yield self._request_page(date_str, page, self.parse)

    def parse(self, response):
        rows = response.xpath('//table[@class="tabla"]/tr[@height="30"]')

        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        for row in rows:
            l = ManoloItemLoader(item=ManoloItem(), selector=row)

            l.add_value('institution', 'presidencia')
            l.add_value('date', date)

            l.add_xpath('full_name', './/td[3]/text()')

            l.add_xpath('entity', './/td[5]/text()')

            l.add_xpath('reason', './/td[6]/text()')
            l.add_xpath('host_name', './/td[7]/text()')

            l.add_xpath('time_start', './/td[9]/text()')
            l.add_xpath('time_end', './/td[10]/text()')
            l.add_xpath('meeting_place', './/td[11]/text()')

            document_identity = row.xpath('.//td[4]/text()').extract_first(default='')
            id_document, id_number = get_dni(document_identity)

            l.add_value('id_number', id_number)
            l.add_value('id_document', id_document)

            office_title = row.xpath('.//td[8]/text()').extract_first(default='')
            office_title = office_title.split('-')

            try:
                l.add_value('office', office_title[0])
                l.add_value('title', office_title[1])
            except IndexError:
                pass

            item = l.load_item()

            item = make_hash(item)

            yield item
