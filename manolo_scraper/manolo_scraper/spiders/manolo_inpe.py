# -*- coding: utf-8 -*-
import scrapy


class INPESpider(scrapy.Spider):
    name = "inpe"
    allowed_domains = ["example.com"]
    start_urls = (
        'http://www.example.com/',
    )

    def parse(self, response):
        pass
