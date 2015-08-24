# -*- coding: utf-8 -*-
import os
import unittest

from manolo_scraper.spiders.inpe import INPESpider
from manolo_scraper.utils import make_hash
from utils import fake_response_from_file


class TestINPESpider(unittest.TestCase):

    def setUp(self):
        self.spider = INPESpider()

    def test_parse_item(self):
        filename = os.path.join('data/inpe', '19-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'19/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'MARIA DEL PILAR LLUEN MACALOPU')
        self.assertEqual(item.get('time_start'), u'08:39:00')
        self.assertEqual(item.get('institution'), u'inpe')
        self.assertEqual(item.get('id_document'), u'DNI/LE')
        self.assertEqual(item.get('id_number'), u'17434996')
        self.assertEqual(item.get('entity'), u'Particular')
        self.assertEqual(item.get('reason'), u'Reunion')
        self.assertEqual(item.get('host_name'), u'MILAGROS MAGDALENA MU\xc3\u2018OZ GONZALES')
        self.assertEqual(item.get('title'), u'---')
        self.assertEqual(item.get('office'), u'Unidad De Recursos Humanos')
        self.assertEqual(item.get('time_end'), u'08:54:00')
        self.assertEqual(item.get('date'), u'2015-08-19')

        number_of_items = 1 + sum(1 for _ in items)
        self.assertEqual(number_of_items, 60)

    def test_correct_hash_sha1_for_legacy_data(self):
        item = {
            'full_name': 'Victor Alberto Menacho Aguinaga',
            'entity': 'E.P.Ancon 1',
            'meeting_place': '',
            'office': 'Unidad De Recursos Humanos',
            'host_name': 'WENDY DIANA HINOSTROZA HUARANGA',
            'reason': 'DOCUMENTACION',
            'institution': 'inpe',
            'location': '',
            'id_number': '42000454',
            'id_document': 'DNI/LE',
            'date': '2011-08-01',
            'time_start': '11:35',
            'time_end': '11:49',
            'objective': 'Documentacion',
            'num_visit': '',
            'title': '',
        }
        result = make_hash(item)
        expected = 'cad139c1cc501911d881edc6587f0ce887c2d6ce'
        self.assertEqual(expected, result['sha1'])
