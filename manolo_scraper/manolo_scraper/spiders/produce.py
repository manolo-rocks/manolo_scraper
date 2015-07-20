# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta

import scrapy
from scrapy import exceptions

from manolo_scraper.items import ManoloItem
from manolo_scraper.utils import make_hash


class ProduceSpider(scrapy.Spider):
    name = "produce"
    allowed_domains = ["http://www2.produce.gob.pe"]

    def __init__(self, date_start=None, *args, **kwargs):
        super(ProduceSpider, self).__init__(*args, **kwargs)
        self.date_start = date_start
        if self.date_start is None:
            raise exceptions.UsageError('Enter start date as spider argument: -a date_start=')

    def start_requests(self):
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        # d2 = datetime.date(2015, 1, 15)
        d2 = datetime.date.today()
        # range to fetch
        delta = d2 - d1

        for i in range(delta.days + 1):
            my_date = d1 + timedelta(days=i)
            my_date_str = my_date.strftime("%d/%m/%Y")
            print("SCRAPING: %s" % my_date_str)

            request = scrapy.FormRequest("http://www2.produce.gob.pe/produce/transparencia/visitas/",
                                         formdata={'desFecha': my_date_str,
                                                   'desFechaF': my_date_str,
                                                   'buscar': 'Consultar'},
                                         callback=self.parse)
            request.meta['date'] = my_date
            yield request

    def parse(self, response):
        for sel in response.xpath('//tr'):
            this_record = sel.xpath('td')
            if len(this_record) > 9:
                item = ManoloItem()
                item['full_name'] = ''
                item['id_document'] = ''
                item['id_number'] = ''
                item['institution'] = 'produce'
                item['entity'] = ''
                item['reason'] = ''
                item['host_name'] = ''
                item['title'] = ''
                item['office'] = ''
                item['time_start'] = ''
                item['time_end'] = ''
                item['date'] = response.meta['date']

                try:
                    item['time_start'] = this_record[2].xpath('text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['full_name'] = this_record[3].xpath('text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['id_document'] = this_record[4].xpath('text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['id_number'] = this_record[5].xpath('text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['reason'] = this_record[6].xpath('text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['host_name'] = this_record[7].xpath('text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['office'] = this_record[8].xpath('text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['time_end'] = this_record[9].xpath('text()').extract()[0]
                except IndexError:
                    pass

                item = make_hash(item)

                yield item
