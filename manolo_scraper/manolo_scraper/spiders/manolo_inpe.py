# -*- coding: utf-8 -*-
import scrapy

from manolo_scraper.items import ManoloItem


class INPESpider(scrapy.Spider):
    name = "inpe"
    allowed_domains = ["www.peru.gob.pe",
                       "visitasadm.inpe.gob.pe"]

    def start_requests(self):
        return [scrapy.FormRequest("http://visitasadm.inpe.gob.pe/VisitasadmInpe/Controller",
                                   formdata={'vis_fec_ing': '01/12/2014'},
                                   callback=self.parse)]

    def parse(self, response):
        item = ManoloItem()
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
            if len(fields) > 1:
                item['time_start'] = fields[1]
                item['full_name'] = fields[2]
                item['id_document'] = fields[3]
                item['id_number'] = fields[4]
                item['entity'] = fields[5]
                item['reason'] = fields[6]
                item['host_name'] = fields[7]
                item['title'] = fields[8]
                item['office'] = fields[9]
                item['time_start'] = fields[1]
                item['time_start'] = fields[1]
