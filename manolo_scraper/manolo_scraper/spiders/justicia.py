import logging

from scrapy import FormRequest

from spiders import ManoloBaseSpider
from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import make_hash


class JusticiaSpider(ManoloBaseSpider):
    name = 'justicia'
    allowed_domains = ['http://visitas.minjus.gob.pe']
    base_url = 'http://visitas.minjus.gob.pe/visita_web'

    def initial_request(self, date):
        date_str = date.strftime('%d/%m/%Y')
        request = self._request_number_of_pages(date_str)
        return request

    def _request_number_of_pages(self, date_str):
        url = self.base_url + '/consulta_paginarBusquedaVisitas'

        request = FormRequest(url=url,
                              meta={
                                  'date': date_str,
                              },
                              formdata={
                                  'fechaDesde': date_str,
                                  'fechaHasta': date_str,
                                  'paginaActual': '1',
                                  'visita.visitanteNombres': '',
                                  'visita.personalNombre': '',
                                  'visita.oficinaNombre': '',
                                  'visita.sedeId': '00',
                                  'visita.ano': '',
                                  'visita.mes': '',
                                  'visita.fechaIngreso': '',
                                  'paginaNueva': '0',
                                  'visita.visitanteId': '0',
                                  'visita.personalId': '0',
                                  'visita.oficinaId': '0',
                              },
                              dont_filter=True,
                              callback=self.parse_initial_request)

        request.meta['date'] = date_str
        return request

    def parse_initial_request(self, response):
        date_str = response.meta['date']

        number_of_pages = response.xpath('//select/option/text()').extract()

        if number_of_pages:
            number_of_pages = int(number_of_pages[-1])

            for page in range(1, number_of_pages + 1):
                request = self._request_page(date_str, page, self.parse)

                yield request

    def _request_page(self, date_str, page, callback):
        url = self.base_url + '/consulta_buscarVisitas'

        request = FormRequest(url=url,
                              meta={
                                  'date': date_str,
                              },
                              formdata={
                                  'fechaDesde': date_str,
                                  'fechaHasta': date_str,
                                  'paginaActual': str(page),
                                  'visita.visitanteNombres': '',
                                  'visita.personalNombre': '',
                                  'visita.oficinaNombre': '',
                                  'visita.sedeId': '00',
                                  'visita.ano': '',
                                  'visita.mes': '',
                                  'visita.fechaIngreso': '',
                                  'paginaNueva': str(page),
                                  'visita.visitanteId': '0',
                                  'visita.personalId': '0',
                                  'visita.oficinaId': '0',
                              },
                              dont_filter=True,
                              callback=callback)
        return request

    def parse(self, response):
        rows = response.xpath('//table/tr')
        date = self.get_date_item(response.meta['date'], '%d/%m/%Y')

        for row in rows:
            warnings = []
            l = ManoloItemLoader(item=ManoloItem(), selector=row)

            l.add_value('institution', 'minjus')
            l.add_value('date', date)

            l.add_xpath('full_name', './/td[4]/br/preceding-sibling::node()/self::text()')

            l.add_xpath('entity', './/td[4]/b/following-sibling::node()/self::text()')

            l.add_xpath('reason', './/td[6]/br/preceding-sibling::node()/self::text()')
            l.add_xpath('host_name', './/td[7]/br/preceding-sibling::node()/self::text()')
            l.add_xpath('office', './/td[7]/b/following-sibling::node()/self::text()')

            l.add_xpath('location', './/td[1]/text()')

            l.add_xpath('id_document', './/td[5]/br/preceding-sibling::node()/self::text()')
            try:
                l.add_xpath('id_number', './/td[5]/br/following-sibling::node()/self::text()')
            except KeyError as e:
                warnings.append("No id number, error: {} for item: ".format(e))

            time_start_time_end = row.xpath(
                './/td[2]/div/br/following-sibling::node()/self::text()',
            ).extract_first(default='')

            time_start_time_end = time_start_time_end.split('-')

            try:
                l.add_value('time_start', time_start_time_end[0])
            except IndexError:
                warnings.append("No time_start for item: ")

            try:
                l.add_value('time_end', time_start_time_end[1])
            except IndexError:
                warnings.append("No time_end for item: ")

            item = l.load_item()
            item = make_hash(item)

            if warnings:
                for i in warnings:
                    logging.warning("{0}{1}".format(i, item))

            yield item
