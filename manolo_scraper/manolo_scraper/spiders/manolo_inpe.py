# -*- coding: utf-8 -*-
import datetime
from datetime import date
from datetime import timedelta

import sqlite3
import scrapy

from manolo_scraper.items import ManoloItem
from manolo_scraper.models import db_connect


class INPESpider(scrapy.Spider):
    name = "inpe"
    allowed_domains = ["www.peru.gob.pe",
                       "visitasadm.inpe.gob.pe"]

    def start_requests(self):
        """
        Get starting date to scrape from our database

        :return: set of URLs
        """
        last_date_in_db = ''

        db = db_connect()

        query = "select distinct date from manolo_inpe_manolo order by date desc limit 1"
        try:
            res = db.query(query)
            for i in res:
                last_date_in_db = i['date']
        except sqlite3.OperationalError:
            pass

        if last_date_in_db == '':
            last_date_in_db = '2011-07-28'

        d1 = datetime.datetime.strptime(last_date_in_db, '%Y-%m-%d').date()
        d2 = date.today()
        # range to fetch
        delta = d2 - d1

        for i in range(delta.days + 1):
            my_date = d1 + timedelta(days=i)
            my_date_str = my_date.strftime("%d/%m/%Y")
            print("SCRAPING: %s" % my_date)

            request = scrapy.FormRequest("http://visitasadm.inpe.gob.pe/VisitasadmInpe/Controller",
                                      formdata={'vis_fec_ing': my_date_str},
                                      callback=self.parse)
            request.meta['date'] = my_date
            yield  request

    def parse(self, response):
        item = ManoloItem()
        item['date'] = response.meta['date']
        item['full_name'] = ''
        item['id_document'] = ''
        item['id_number'] = ''
        item['institution'] = ''
        item['entity'] = ''
        item['reason'] = ''
        item['host_name'] = ''
        item['title'] = ''
        item['office'] = ''
        item['time_start'] = ''
        item['time_end'] = ''

        selectors = response.xpath("//tr")
        for sel in selectors:
            fields = sel.xpath("td/text() | td/p/text()").extract()
            if len(fields) > 7:
                item['time_start'] = fields[1]
                item['full_name'] = fields[2]
                item['id_document'] = fields[3]
                item['id_number'] = fields[4]
                item['entity'] = fields[5]
                item['reason'] = fields[6]
                item['host_name'] = fields[7]
                item['title'] = fields[8]
                item['time_start'] = fields[1]
                item['time_start'] = fields[1]
                try:
                    item['office'] = fields[9]
                except IndexError:
                    item['office'] = ''

                yield item

