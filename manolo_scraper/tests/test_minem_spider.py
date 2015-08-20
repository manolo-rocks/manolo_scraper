# -*- coding: utf-8 -*-
import os
import unittest

from manolo_scraper.spiders.minem import MinemSpider
from manolo_scraper.utils import make_hash
from utils import fake_response_from_file


class TestMinemSpider(unittest.TestCase):

    def setUp(self):
        self.spider = MinemSpider()

    def test_parse_item(self):
        filename = os.path.join('data/minem', '19-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'19/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'CARMEN ALICIA GUTIERREZ VELASCO')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'08241251')
        self.assertEqual(item.get('entity'), u'ESLOM')
        self.assertEqual(item.get('reason'), u'REUNI\xc3\u201cN DE TRABAJO')
        self.assertEqual(item.get('host_name'), u'OMAR FRANCO CHAMBERGO RODRIGUEZ')
        self.assertEqual(item.get('office'), u'DIRECCION GENERAL DE HIDROCARBUROS-N')
        self.assertEqual(item.get('time_start'), u'08:01')
        self.assertEqual(item.get('time_end'), u'08:17')
        self.assertEqual(item.get('meeting_place'), u'OFICINA DEL FUNCIONARIO')
        self.assertEqual(item.get('institution'), u'minem')
        self.assertEqual(item.get('date'), u'2015-08-19')
        self.assertEqual(item.get('sha1'), u'fa5238c796089a49ed8583ce36457c30e5e58e05')

        number_of_items = 1 + sum(1 for _ in items)

        self.assertEqual(number_of_items, 20)

    def test_correct_hash_sha1_for_legacy_data(self):
        item = {
            'date': '2012-01-04',
            'entity': u'PARTICULAR',
            'full_name': u'BUENO NINAHUANCA, JHON BILL',
            'host_name': u'RIVAS CIFUENTES, BENJAMIN DIONISIO',
            'id_document': u'DNI',
            'id_number': u'40748332',
            'institution': u'minem',
            'location': '',
            'meeting_place': '',
            'office': u'DGER - SALA DEP',
            'reason': u'CONSULTA CIUDADANA',
            'time_start': u'08:39',
            'time_end': u'',
            'title': u'Especialista I',
        }
        result = make_hash(item)
        expected = '09dc4688afd00bb9ba60e69a4d1369b09dc261cf'
        self.assertEqual(expected, result['sha1'])
