# -*- coding: utf-8 -*-
import logging

from scrapy import Request, FormRequest

from spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash, get_dni


class PresidenciaSpider(ManoloBaseSpider):
    name = 'presidencia'
    allowed_domains = ['presidencia.gob.pe']
    base_url = 'http://transparencia.presidencia.gob.pe/visitas'

    # custom_settings = {
        # "HTTP_PROXY": "http://127.0.0.1:8118",
    # }

    def initial_request(self, date):
        date_str = date.strftime('%d/%m/%Y')

        request = self._request_page(date_str, self.parse)

        return request

    def _request_page(self, date_str, callback):
        url = self.base_url + '/index_server.php'
        request = FormRequest(
            url=url,
            meta={
                'date': date_str,
            },
            formdata={"valorCaja1": date_str},
            dont_filter=True,
            callback=callback,
        )
        request.meta['date'] = date_str
        return request


    def parse(self, response):
        with open("a.html", "w") as handle:
            handle.write(response.body)
        rows = response.xpath('//tr')

        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        for row in rows:
            if len(row.xpath(".//td")) < 4:
                continue
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

            warnings = []
            try:
                l.add_value('office', office_title[0])
            except IndexError:
                warnings.append("No office for item: ")

            try:
                l.add_value('title', office_title[1])
            except IndexError:
                warnings.append("No title for item: ")

            item = l.load_item()
            item = make_hash(item)

            if warnings:
                for i in warnings:
                    logging.warning("{0}{1}".format(i, item))

            yield item
