# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta

import scrapy

from manolo_scraper.spiders.tc import TcSpider


class TcSpiderLocal(TcSpider):
    name = "tc_local"
    allowed_domains = ["127.0.0.1"]

    def start_requests(self):
        end_date = datetime.date.today()
        delta = end_date - self.start_date

        for i in range(delta.days + 1):
            this_date = self.start_date + timedelta(days=i)
            this_date_str = datetime.datetime.strftime(this_date, '%Y-%m-%d')
            url = 'http://127.0.0.1:8000/html_tc/page_' + this_date_str + '_.html'
            request = scrapy.Request(url, callback=self.parse)
            request.meta['date'] = this_date
            yield request
