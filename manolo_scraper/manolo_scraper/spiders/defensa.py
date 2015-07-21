# -*- coding: utf-8 -*-
import datetime
import logging

import scrapy
from scrapy import exceptions


class DefensaSpider(scrapy.Spider):
    name = "defensa"
    allowed_domains = ["mindef.gob.pe"]

    def __init__(self, date_start=None, *args, **kwargs):
        super(DefensaSpider, self).__init__(*args, **kwargs)
        self.date_start = date_start
        if self.date_start is None:
            raise exceptions.UsageError('Enter start date as spider argument: -a date_start=')

    def start_requests(self):
        d1 = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
        d2 = datetime.date.today()
        delta = d2 - d1

        for i in range(delta.days + 1):
            my_date = d1 + datetime.timedelta(days=i)
            my_date_str = my_date.strftime("%d/%m/%Y")
            logging.info("SCRAPING: {}".format(my_date_str))

            params = {'fechaqry': my_date_str}
            url = "http://www.mindef.gob.pe/visitas/qryvisitas.php"
            yield scrapy.FormRequest(url=url, formdata=params,
                                     meta={'date': my_date_str},
                                     dont_filter=True,
                                     callback=self.after_post)
    def after_post(self, response):
        # send requests based on pagination
        pass

    def parse(self, response):
        pass
