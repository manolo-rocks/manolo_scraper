# -*- coding: utf-8 -*-
import datetime
from datetime import date
from datetime import timedelta
import hashlib

import sqlite3
import scrapy

from manolo_scraper.items import ManoloItem
from manolo_scraper.models import db_connect
from manolo_scraper.utils import make_hash


class INPESpider(scrapy.Spider):
    name = "inpe"
    allowed_domains = ["www.peru.gob.pe",
                       "visitasadm.inpe.gob.pe"]

    def __init__(self, date_start=None, *args, **kwargs):
        super(INPESpider, self).__init__(*args, **kwargs)
        self.date_start = date_start

    def start_requests(self):
        """
        Get starting date to scrape from argument
        e.g.: 2010-02-21

        :return: set of URLs
        """

        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
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
            yield request

    def parse(self, response):
        #with open("page_" + response.meta['date'].strftime("%d-%m-%Y") + "_.html", "w") as handle:
            #handle.write(response.body)
        item = ManoloItem()
        item['full_name'] = ''
        item['id_document'] = ''
        item['id_number'] = ''
        item['institution'] = 'inpe'
        item['entity'] = ''
        item['reason'] = ''
        item['host_name'] = ''
        item['title'] = ''
        item['office'] = ''
        item['time_start'] = ''
        item['time_end'] = ''

        selectors = response.xpath("//tr")
        for sel in selectors:
            fields = sel.xpath("td/p")
            if len(fields) > 7:
                # This is a sentinel to flag it as scraped item
                item['date'] = response.meta['date']

                item['full_name'] = fields[0].xpath("text()").extract()[0].strip()

                try:
                    item['id_document'] = fields[1].xpath("text()").extract()[0].strip()
                except IndexError:
                    item['id_document'] = ''

                item['id_number'] = fields[2].xpath("text()").extract()[0].strip()
                item['entity'] = fields[3].xpath("text()").extract()[0].strip()
                item['reason'] = fields[4].xpath("text()").extract()[0].strip()
                item['host_name'] = fields[5].xpath("text()").extract()[0].strip()
                item['title'] = fields[6].xpath("text()").extract()[0].strip()
                item['office'] = fields[7].xpath("text()").extract()[0].strip()

            times = sel.xpath("td")
            if len(times) > 10:
                item['time_start'] = times[1].xpath("text()").extract()[0].strip()

                time_end = times[10].xpath("text()").extract()
                if len(time_end) > 0:
                    item['time_end'] = time_end[0]
                else:
                    item['time_end'] = ''

                try:
                    x = datetime.datetime.strptime(item['time_start'], '%H:%M:%S')
                    item['time_start'] = datetime.datetime.strftime(x, '%H:%M')
                except ValueError:
                    pass

                try:
                    x = datetime.datetime.strptime(item['time_end'], '%H:%M:%S')
                    item['time_end'] = datetime.datetime.strftime(x, '%H:%M')
                except ValueError:
                    pass

                item = make_hash(item)

            # Our item has the sentinel?
            if 'date' in item:
                yield item

