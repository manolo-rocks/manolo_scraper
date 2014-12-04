# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ManoloItem(scrapy.Item):
    date = scrapy.Field()
    full_name = scrapy.Field()  # Full name of visitor
    id_document = scrapy.Field()  # DNI, Brevete?
    id_number = scrapy.Field()
    institution = scrapy.Field()  # institution visited: OSCE, Vivienda?
    entity = scrapy.Field()  # Entity that the visitor represents
    reason = scrapy.Field()  # Reason behind the meeting
    host_name = scrapy.Field()  # Name of person that receives visitor
    title = scrapy.Field()  # Official title of host person, "cargo"
    office = scrapy.Field()  # Office that visitor visits
    time_start = scrapy.Field()
    time_end = scrapy.Field()
