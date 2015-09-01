# -*- coding: utf-8 -*-
import os
import unittest

from manolo_scraper.spiders.mujer import MujerSpider
from manolo_scraper.utils import make_hash
from utils import fake_response_from_file


class TestMujerSpider(unittest.TestCase):

    def setUp(self):
        self.spider = MujerSpider()

    def test_parse_item(self):
        filename = os.path.join('data/mujer', '20-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'20/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'VIGO LOPEZ BETTY CATHERINE')
        self.assertEqual(item.get('time_start'), u'07:56 AM')
        self.assertEqual(item.get('institution'), u'min. mujer')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'43521527')
        self.assertEqual(item.get('entity'), u'SAN MIGUEL')
        self.assertEqual(item.get('reason'), None)
        self.assertEqual(item.get('host_name'), u'PNCVFS ,')
        self.assertEqual(item.get('office'), u'PROGRAMA NACIONAL CONTRA LA VIOLENCIA FAMILIAR Y SEXUAL')
        self.assertEqual(item.get('time_end'), u'10:42 AM')
        self.assertEqual(item.get('date'), u'2015-08-20')
        self.assertEqual(item.get('sha1'), u'a00e952857d8c86ab3877ee3805bda686bd3a999')

        number_of_items = 1 + sum(1 for x in items)
        self.assertEqual(number_of_items, 20)

    def test_correct_hash_sha1_for_legacy_data(self):
        item = {
            'full_name': u'FIGUEROA BERMUDEZ FRANKLIN',
            'entity': u'SCOTIABANK',
            'meeting_place': '',
            'office': u'DESPACHO VICE - MINISTERIAL DE LA MUJER',
            'host_name': u'CENTRO DOCUMENTARIO',
            'reason': '',
            'institution': u'min. mujer',
            'location': '',
            'id_number': u'42982496',
            'id_document': u'DNI',
            'date': u'2012-02-29',
            'time_start': u'12:33',
            'time_end': u'13:18',
            'objective': '',
            'num_visit': '',
            'title': '',
        }
        result = make_hash(item)
        expected = '50aa11295b04317f97e6e27dcb965c50d3e78a3b'
        self.assertEqual(expected, result['sha1'])
