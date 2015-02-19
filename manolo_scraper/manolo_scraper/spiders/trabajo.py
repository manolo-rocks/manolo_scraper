# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta

import scrapy

from manolo_scraper.items import ManoloItem
from manolo_scraper.utils import make_hash


class TrabajoSpider(scrapy.Spider):
    name = "trabajo"
    allowed_domains = ["http://visitas.trabajo.gob.pe"]

    def start_requests(self):
        # d1 = datetime.date(2012, 8, 1)
        d1 = datetime.date(2015, 2, 19)
        # d2 = datetime.date(2015, 1, 15)
        d2 = datetime.date.today()
        # range to fetch
        delta = d2 - d1

        for i in range(delta.days + 1):
            my_date = d1 + timedelta(days=i)
            my_date_str = my_date.strftime("%d/%m/%Y")
            print("SCRAPING: %s" % my_date_str)

            request = scrapy.FormRequest("http://visitas.trabajo.gob.pe:8080/si.sigevi/doReporte.do",
                                         formdata={'method': 'visitasMtpe',
                                                   'v_fecini': my_date_str},
                                         callback=self.parse)
            request.meta['date'] = my_date
            yield request

    def parse(self, response):
        with open("trabajo_page_" + response.meta['date'].strftime("%d-%m-%Y") + ".html", "w") as handle:
            handle.write(response.body)

        for sel in response.xpath('//tr'):
            this_record = sel.xpath('td')
            if len(this_record) > 9:
                item = ManoloItem()
                item['full_name'] = ''
                item['id_document'] = ''
                item['id_number'] = ''
                item['institution'] = 'trabajo'
                item['entity'] = ''
                item['reason'] = ''
                item['host_name'] = ''
                item['title'] = ''
                item['office'] = ''
                item['time_start'] = ''
                item['time_end'] = ''
                item['date'] = response.meta['date']

                try:
                    item['full_name'] = this_record[1].xpath('text()').extract()[0]
                except IndexError:
                    pass

                try:
                    document = this_record[2].xpath('text()').extract()[0]
                except IndexError:
                    pass

                if document is not None:
                    document = document.split(" ")
                    item['id_document'] = document[0]
                    item['id_number'] = document[1]

                try:
                    item['entity'] = this_record[3].xpath('text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['reason'] = this_record[4].xpath('text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['host_name'] = this_record[5].xpath('text()').extract()[0]
                except IndexError:
                    pass

                try:
                    item['meeting_place'] = this_record[6].xpath('text()').extract()[0]
                except IndexError:
                    pass



                try:
                    item['time_start'] = this_record[2].xpath('text()').extract()[0]
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
