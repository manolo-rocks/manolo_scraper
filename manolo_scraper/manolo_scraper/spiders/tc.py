# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta
import hashlib
from unidecode import unidecode
import re
import sys

import scrapy

from manolo_scraper.items import ManoloItem


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
            this_month = get_this_month(datetime.datetime.strftime(this_date, '%m'))
            this_date_str = datetime.datetime.strftime(this_date, '%d%m%Y')
            url = "http://tc.gob.pe/transparencia/visitas/"
            url += this_year + "/"
            url += this_month + "/"
            url += this_date_str + ".html"
            request = scrapy.Request(url, callback=self.parse)
            request.meta['date'] = this_date
            yield request

    def parse(self, response):
        this_date = response.meta['date']
        for sel in response.xpath('//tr'):
            record = sel.xpath('td/text()').extract()
            if len(record) > 6:
                if this_date < datetime.date(2008, 5, 29):
                    item = ManoloItem()
                    item['full_name'] = record[2]
                    item['id_document'] = record[3]
                    item['id_number'] = record[4]
                    item['reason'] = record[5]
                    item['host_name'] = record[6]
                    try:
                        item['time_start'] = record[1].replace('.', ':')
                    except AttributeError:
                        item['time_start'] = record[1]

                    try:
                        item['time_end'] = record[8].replace('.', ':')
                    except AttributeError:
                        item['time_end'] = record[8]

                    item['institution'] = 'Trib.Const.'
                    item['date'] = response.meta['date']

                    item = make_hash(item)
                    yield item
                elif datetime.date(2008, 5, 29) <= this_date < datetime.date(2014, 8, 1):
                    item = ManoloItem()
                    item['full_name'] = record[2]
                    item['id_document'] = record[3]
                    item['id_number'] = record[4]
                    item['reason'] = record[5]
                    item['host_name'] = record[6]
                    try:
                        item['time_start'] = record[1].replace('.', ':')
                    except AttributeError:
                        item['time_start'] = record[1]

                    try:
                        item['time_end'] = record[7].replace('.', ':')
                    except AttributeError:
                        item['time_end'] = record[7]

                    item['institution'] = 'Trib.Const.'
                    item['date'] = response.meta['date']

                    item = make_hash(item)
                    yield item
                else:
                    print(record)
                    item = ManoloItem()
                    item['full_name'] = record[1]
                    item['id_document'], item['id_number'] = get_dni(record[2])
                    item['entity'] = record[3]
                    item['reason'] = record[4]
                    item['host_name'] = record[5]
                    item['office'] = record[6]
                    try:
                        item['time_start'] = record[7].replace('.', ':')
                    except AttributeError:
                        item['time_start'] = record[7]

                    try:
                        item['time_end'] = record[8].replace('.', ':')
                    except AttributeError:
                        item['time_end'] = record[8]

                    item['institution'] = 'Trib.Const.'
                    item['date'] = response.meta['date']

                    item = make_hash(item)
                    yield item



def make_hash(item):
    hash_input = str(
        str(item['institution']) +
        str(unidecode(item['full_name'])) +
        str(item['id_document']) +
        str(item['id_number']) +
        str(item['date']) +
        str(item['time_start'])
    )
    hash_output = hashlib.sha1()
    hash_output.update(hash_input.encode("utf-8"))
    item['sha1'] = hash_output.hexdigest()
    return item


def get_dni(document_identity):
    id_document = ''
    id_number = ''

    document_identity = document_identity.replace(':', ' ')
    document_identity = re.sub('\s+', ' ', document_identity)
    document_identity = document_identity.strip()
    document_identity = re.sub('^', ' ', document_identity)

    res = re.search("(.*)\s(([A-Za-z0-9]+\W*)+)$", document_identity)
    if res:
        id_document = res.groups()[0].strip()
        id_number = res.groups()[1].strip()

    if id_document == '':
        id_document = 'DNI'

    return id_document, id_number


def get_this_month(number):
    if number == '01':
        return 'enero'
    elif number == '02':
        return 'febrero'
    elif number == '03':
        return 'marzo'
    elif number == '04':
        return 'abril'
    elif number == '05':
        return 'manyo'
    elif number == '06':
        return 'junio'
    elif number == '07':
        return 'julio'
    elif number == '08':
        return 'agosto'
    elif number == '09':
        return 'setiembre'
    elif number == '10':
        return 'octubre'
    elif number == '11':
        return 'noviembre'
    elif number == '12':
        return 'diciembre'
