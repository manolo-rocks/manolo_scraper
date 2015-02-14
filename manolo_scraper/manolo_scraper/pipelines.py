# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['sha1'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['sha1'])
            return item


class CleanItemPipeline(object):
    def process_item(self, item, spider):
        for k, v in item.items():
            if isinstance(v, basestring) is True:
                value = re.sub('\s+', ' ', v)
                item[k] = value.strip()
            else:
                item[k] = v
        if item['full_name'] == '':
            raise DropItem("Missing visitor in %s" % item)

        if item['time_start'].starts_with('HORA DE'):
            raise DropItem("This is a header, drop it: %s" % item)
        return item
