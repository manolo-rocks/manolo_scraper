# -*- coding: utf-8 -*-
import scrapy

from ..items import FileItem


class EssaludSpider(scrapy.Spider):
    name = "essalud"
    allowed_domains = ["essalud.gob.pe"]
    start_urls = (
        'http://www.essalud.gob.pe/registro-de-visitas/',
    )

    def parse(self, response):
        item = FileItem()
        item["file_urls"] = []
        for link in response.xpath("//a"):
            link_text = link.xpath("text()").extract_first()
            if link_text and "Registro" in link_text:
                url = link.xpath("./@href").extract_first()
                if url.startswith("/"):
                    url = "http://www.essalud.gob.pe" + url
                if url.endswith(".xls"):
                    item["file_urls"].append(url)
        yield item
