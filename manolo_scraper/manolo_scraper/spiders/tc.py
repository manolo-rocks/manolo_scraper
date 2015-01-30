# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta
import sys

import scrapy

from manolo_scraper.items import ManoloItem
from manolo_scraper import utils


class TcSpider(scrapy.Spider):
    name = "tc"
    allowed_domains = ["www.tc.gob.pe"]
    start_urls = (
        'http://www.www.tc.gob.pe/',
    )

    def __init__(self, start_date=None, *args, **kwargs):
        super(TcSpider, self).__init__(*args, **kwargs)
        if start_date is None:
            print("Need to enter start_date as argument: `-a start_date=2014-01-01`")
            sys.exit(0)
        print("Start date arg", start_date)
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

    def start_requests(self):
        end_date = datetime.date.today()
        delta = end_date - self.start_date

        for i in range(delta.days + 1):
            this_date = self.start_date + timedelta(days=i)
            this_year = datetime.datetime.strftime(this_date, '%Y')
            this_month = utils.get_this_month(datetime.datetime.strftime(this_date, '%m'))
            this_date_str = datetime.datetime.strftime(this_date, '%d%m%Y')
            url = "http://tc.gob.pe/transparencia/visitas/"
            url += this_year + "/"
            url += this_month + "/"

            if this_date < datetime.date(2009, 8, 1):
                url += this_date_str + ".htm"
            else:
                url += this_date_str + ".html"
            request = scrapy.Request(url, callback=self.parse)
            request.meta['date'] = this_date
            yield request

    def parse(self, response):
        with open("page_" + response.meta['date'].strftime("%Y-%m-%d") + "_.html", "w") as handle:
            handle.write(response.body)
        this_date = response.meta['date']
        for sel in response.xpath('//tr'):
            record = sel.xpath('td/text()').extract()
            if len(record) > 6:
                if this_date < datetime.date(2008, 5, 29):
                    item = ManoloItem()
                    try:
                        item['full_name'] = sel.xpath('td')[2].xpath('text()').extract()[0]
                    except IndexError:
                        item['full_name'] = ''

                    try:
                        item['id_document'] = sel.xpath('td')[3].xpath('text()').extract()[0]
                    except IndexError:
                        item['id_document'] = ''

                    try:
                        item['id_number'] = sel.xpath('td')[4].xpath('text()').extract()[0]
                    except IndexError:
                        item['id_number'] = ''

                    try:
                        item['reason'] = sel.xpath('td')[5].xpath('text()').extract()[0]
                    except IndexError:
                        item['reason'] = ''

                    try:
                        item['host_name'] = sel.xpath('td')[6].xpath('text()').extract()[0]
                    except IndexError:
                        item['host_name'] = ''

                    try:
                        item['time_start'] = sel.xpath('td')[1].xpath('text()').extract()[0]
                    except IndexError:
                        item['time_start'] = ''

                    try:
                        item['time_end'] = sel.xpath('td')[8].xpath('text()').extract()[0]
                    except IndexError:
                        item['time_end'] = ''

                    item['institution'] = 'Trib.Const.'
                    item['date'] = response.meta['date']

                    item = utils.make_hash(item)
                    yield item
                elif datetime.date(2008, 5, 29) <= this_date < datetime.date(2014, 8, 1):
                    item = ManoloItem()
                    try:
                        item['full_name'] = sel.xpath('td')[2].xpath('text()').extract()[0]
                    except IndexError:
                        item['full_name'] = ''

                    try:
                        item['id_document'] = sel.xpath('td')[3].xpath('text()').extract()[0]
                    except IndexError:
                        item['id_document'] = ''

                    try:
                        item['id_number'] = sel.xpath('td')[4].xpath('text()').extract()[0]
                    except IndexError:
                        item['id_number'] = ''

                    try:
                        item['reason'] = sel.xpath('td')[5].xpath('text()').extract()[0]
                    except IndexError:
                        item['reason'] = ''

                    try:
                        item['host_name'] = sel.xpath('td')[6].xpath('text()').extract()[0]
                    except IndexError:
                        item['host_name'] = ''

                    try:
                        item['time_start'] = sel.xpath('td')[1].xpath('text()').extract()[0]
                    except IndexError:
                        item['time_start'] = ''

                    try:
                        item['time_end'] = sel.xpath('td')[7].xpath('text()').extract()[0]
                    except IndexError:
                        item['time_end'] = ''

                    item['institution'] = 'Trib.Const.'
                    item['date'] = response.meta['date']

                    item = utils.make_hash(item)
                    yield item
                else:
                    item = ManoloItem()
                    try:
                        item['full_name'] = sel.xpath('td')[1].xpath('text()').extract()[0]
                    except IndexError:
                        item['full_name'] = ''

                    try:
                        item['id_document'], item['id_number'] = utils.get_dni(sel.xpath('td')[2].xpath('text()').extract()[0])
                    except IndexError:
                        item['id_document'] = ''
                        item['id_number'] = ''

                    try:
                        item['entity'] = sel.xpath('td')[3].xpath('text()').extract()[0]
                    except IndexError:
                        item['entity'] = ''

                    try:
                        item['reason'] = sel.xpath('td')[4].xpath('text()').extract()[0]
                    except IndexError:
                        item['reason'] = ''

                    try:
                        item['host_name'] = sel.xpath('td')[5].xpath('text()').extract()[0]
                    except IndexError:
                        item['host_name'] = ''

                    try:
                        item['office'] = sel.xpath('td')[6].xpath('text()').extract()[0]
                    except IndexError:
                        item['office'] = ''

                    try:
                        item['time_start'] = sel.xpath('td')[7].xpath('text()').extract()[0]
                    except IndexError:
                        item['time_start'] = ''

                    try:
                        item['time_end'] = sel.xpath('td')[8].xpath('text()').extract()[0]
                    except IndexError:
                        item['time_end'] = ''

                    item['institution'] = 'Trib.Const.'
                    item['date'] = response.meta['date']

                    item = utils.make_hash(item)
                    yield item
