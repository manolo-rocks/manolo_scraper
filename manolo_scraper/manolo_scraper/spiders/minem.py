# -*- coding: utf-8 -*-
import datetime
from datetime import date
from datetime import timedelta
import re

import scrapy
from scrapy import exceptions

from ..items import ManoloItem
from ..utils import make_hash, get_dni


class MinemSpider(scrapy.Spider):
    name = "minem"
    allowed_domains = ["http://intranet.minem.gob.pe"]

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

            params = [
                'http://intranet.minem.gob.pe/GESTION/visitas_pcm/Busqueda/DMET_html_SelectMaestraBuscador?_=1421960188624',
                'Ln_IdRol=',
                'Ls_Pagina=1',
                'Li_ResultadoPorPagina=2000',
                'FlgBuscador=1',
            ]
            url = "&".join(params) + '&TXT_FechaVisita_Inicio=%s' % my_date_str
            url += '&Ls_ParametrosBuscador=Ln_IdRol=|TXT_FechaVisita_Inicio=%s|Ls_Pagina=1' % my_date_str

            request = scrapy.Request(url, callback=self.parse)
            request.meta['date'] = my_date
            yield request

    def parse(self, response):
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
        item['date'] = response.meta['date']
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
