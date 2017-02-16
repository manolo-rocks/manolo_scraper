# -*- coding: utf-8 -*-
from spiders import SireviSpider

from ..items import ManoloItem
from ..item_loaders import ManoloItemLoader
from ..utils import get_dni


class PcmSpider(SireviSpider):
    name = 'pcm'
    allowed_domains = ['horus.pcm.gob.pe']

    base_url = 'http://horus.pcm.gob.pe/Visitas/controlVisitas'

    institution_name = 'pcm'

    def get_item(self, data, date_str, row):
        l = ManoloItemLoader(item=ManoloItem(), selector=row)

        l.add_value('institution', self.institution_name)
        l.add_value('date', date_str)
        l.add_xpath('full_name', './td[2]/text()')
        l.add_xpath('entity', './td[4]/text()')
        l.add_xpath('reason', './td[5]/text()')
        l.add_xpath('location', './td[6]/text()')
        l.add_xpath('host_name', './td[7]/text()')
        l.add_xpath('office', './td[8]/text()')
        l.add_xpath('meeting_place', './td[9]/text()')
        l.add_xpath('time_start', './td[10]/text()')
        l.add_xpath('time_end', './td[11]/text()')

        try:
            document_identity = data[2].strip()
        except IndexError:
            document_identity = ''

        if document_identity != '':
            id_document, id_number = get_dni(document_identity)

            l.add_value('id_document', id_document)
            l.add_value('id_number', id_number)

        return l.load_item()
