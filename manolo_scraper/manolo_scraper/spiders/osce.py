# -*- coding: utf-8 -*-
import datetime
from datetime import date
from datetime import timedelta
import hashlib
import re
from unidecode import unidecode

import scrapy
import sqlite3

from manolo_scraper.items import ManoloItem
from manolo_scraper.models import db_connect


class OSCESpider(scrapy.Spider):
    name = "osce"
    allowed_domains = ["visitas.osce.gob.pe"]

    def start_requests(self):
        d1 = date(2015, 4, 17)
        d2 = date.today()
        # range to fetch
        delta = d2 - d1

        for i in range(delta.days + 1):
            my_date = d1 + timedelta(days=i)
            my_date_str = my_date.strftime("%d/%m/%Y")
            print("SCRAPING: %s" % my_date_str)

            params = {
                'VisitaConsultaQueryForm[feConsulta]': my_date_str,
                'yt0': 'Consultar',
            }
            url = 'http://visitas.osce.gob.pe/controlVisitas/index.php?r=consultas/visitaConsulta/updateVisitasConsultaResultGrid&ajax=lst-visitas-consulta-result-grid&lstVisitasResult_page='
            url += '1'

            yield scrapy.FormRequest(url=url, formdata=params,
                                     meta={'date': my_date_str},
                                     callback=self.after_post)

    def after_post(self, request):
        dirty_links = re.findall('/controlVisitas.+page=[0-9]+', request.body)
        links = ['http://visitas.osce.gob.pe' + re.sub('".+$', '', i) for i in dirty_links]
        links_set = set(links)
        links_set.add(request.url)

        params = {
            'VisitaConsultaQueryForm[feConsulta]': request.meta['date'],
            'yt0': 'Consultar',
        }
        for link in links_set:
            yield scrapy.FormRequest(url=link, formdata=params,
                                     meta={'date': request.meta['date']},
                                     callback=self.parse)

    def parse(self, response):
        this_date_obj = datetime.datetime.strptime(response.meta['date'],
                                                   '%d/%m/%Y')
        this_date_str = datetime.datetime.strftime(this_date_obj, '%Y-%m-%d')
        with open("page_" + this_date_str + "_.html", "w") as handle:
            handle.write(response.body)
        item = ManoloItem()
        item['full_name'] = ''
        item['entity'] = ''
        item['meeting_place'] = ''
        item['office'] = ''
        item['host_name'] = ''
        item['reason'] = ''
        item['institution'] = 'osce'
        item['location'] = ''
        item['id_number'] = ''
        item['id_document'] = ''
        item['date'] = this_date_obj
        item['title'] = ''
        item['time_start'] = ''
        item['time_end'] = ''

        selectors = response.xpath("//tr")
        for sel in selectors:
            fields = sel.xpath('.//td/text()').extract()

            if len(fields) > 3:
                # full name of visitor
                full_name = re.sub('\s+', ' ', fields[1])
                item['full_name'] = full_name.strip()

                item['entity'] = re.sub("\s+", " ", fields[3]).strip()
                item['reason'] = re.sub("\s+", " ", fields[4]).strip()
                item['host_name'] = re.sub("\s+", " ", fields[5]).strip()

                item['title'] = re.sub("\s+", " ", fields[6]).strip()
                item['office'] = re.sub("\s+", " ", fields[7]).strip()
                item['time_start'] = re.sub("\s+", " ", fields[8]).strip()

                try:
                    document_identity = fields[2].strip()
                except IndexError:
                    document_identity = ''

                if document_identity != '':
                    item['id_document'], item['id_number'] = self.get_dni(document_identity)

                try:
                    item['time_end'] = re.sub("\s+", " ", fields[9]).strip()
                except IndexError:
                    item['time_end'] = ''

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

                yield item

    def get_dni(self, document_identity):
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