# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ManoloItem(scrapy.Item):
    sha1 = scrapy.Field()
    full_name = scrapy.Field()  # Full name of visitor
    entity = scrapy.Field()  # Entity that the visitor represents
    meeting_place = scrapy.Field()  # Location where the meeting is held
    office = scrapy.Field()  # Office that visitor visits, also `unidad`
    host_name = scrapy.Field()  # Name of person that receives visitor
    reason = scrapy.Field()  # Reason behind the meeting
    institution = scrapy.Field()  # institution visited: OSCE, Vivienda?
    location = scrapy.Field()  # Location of institution
    id_number = scrapy.Field()
    id_document = scrapy.Field()  # DNI, Brevete?
    date = scrapy.Field()  # Should be object or string in format YYYY-mm-dd
    title = scrapy.Field()  # Official title of host person, "cargo"
    time_start = scrapy.Field()
    time_end = scrapy.Field()
    created = scrapy.Field()
    modified = scrapy.Field()
