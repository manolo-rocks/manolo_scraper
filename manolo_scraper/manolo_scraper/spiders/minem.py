# -*- coding: utf-8 -*-
import datetime
from datetime import date
from datetime import timedelta
import hashlib
import re

import scrapy
import sqlite3

from manolo_scraper.items import ManoloItem
from manolo_scraper.models import db_connect


class MinemSpider(scrapy.Spider):
    name = "minem"
    allowed_domains = ["http://intranet.minem.gob.pe"]

    def start_requests(self):
        """
        Get starting date to scrape from our database

        :return: set of URLs
        """
        last_date_in_db = ''

        db = db_connect()

        query = "select distinct date from manolo_minem_manolo order by date desc limit 1"
        try:
            res = db.query(query)
            for i in res:
                last_date_in_db = i['date']
        except sqlite3.OperationalError:
            pass

        if last_date_in_db == '':
            last_date_in_db = '2011-07-28'

        d1 = datetime.datetime.strptime(last_date_in_db, '%Y-%m-%d').date()
        d1 = date(2014, 12, 2)
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

    def get_number_items(self, response):
        try:
            number_items = response.xpath("//input/@value").extract()[0]
        except IndexError:
            pass
        url = re.sub('Pagina=20', 'Pagina=' + number_items, response.url)
        print(">>>>>>url", url)
        request = scrapy.Request(url, callback=self.parse)
        request.meta['date'] = response.meta['date']
        yield request

    def parse(self, response):
        with open("page_" + response.meta['date'].strftime("%d-%m-%Y") + "_.html", "w") as handle:
            handle.write(response.body)
        item = ManoloItem()
        item['visitor'] = ''
        item['id_document'] = ''
        item['id_number'] = ''
        item['institution'] = 'minem'
        item['entity'] = ''
        item['reason'] = ''
        item['host_name'] = ''
        item['title'] = ''
        item['office'] = ''
        item['time_start'] = ''
        item['time_end'] = ''

        selectors = response.xpath("//tr")
        for sel in selectors:
            fields = sel.xpath("td/center")

            # This is a sentinel to flag it as scraped item
            item['date'] = response.meta['date']

            visitor = fields[1].xpath("text()").extract()
            try:
                visitor = visitor[0]
            except IndexError:
                pass
            visitor = re.sub("\s+", " ", visitor)
            item['visitor'] = visitor.strip()

            try:
                id_document = fields[2].xpath("text()").extract()[0].strip()
                item['id_document'] = id_document.replace(':', ' ')
            except IndexError:
                item['id_document'] = ''

            item['entity'] = re.sub("\s+", " ", fields[3].xpath("text()").extract()[0].strip())
            item['reason'] = re.sub("\s+", " ", fields[4].xpath("text()").extract()[0].strip())
            item['host_name'] = re.sub("\s+", " ", fields[5].xpath("text()").extract()[0].strip())
            item['title'] = re.sub("\s+", " ", fields[6].xpath("text()").extract()[0].strip())
            item['office'] = re.sub("\s+", " ", fields[7].xpath("text()").extract()[0].strip())
            item['time_start'] = re.sub("\s+", " ", fields[8].xpath("text()").extract()[0].strip())

            try:
                item['time_end'] = re.sub("\s+", " ", fields[9].xpath("text()").extract()[0].strip())
            except IndexError:
                item['time_end'] = ''

            mystring = str(item['date']) + str(item['id_number'])
            mystring += str(item['time_start'])
            m = hashlib.sha1()
            m.update(mystring.encode("utf-8"))
            item['sha512'] = m.hexdigest()

            # Our item has the sentinel?
            if 'date' in item:
                yield item
