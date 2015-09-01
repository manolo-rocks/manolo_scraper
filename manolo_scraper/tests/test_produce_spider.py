# -*- coding: utf-8 -*-
import os
import unittest

from manolo_scraper.spiders.produce import ProduceSpider
from manolo_scraper.utils import make_hash
from utils import fake_response_from_file


class TestProduceSpider(unittest.TestCase):

    def setUp(self):
        self.spider = ProduceSpider()

    def test_parse_item(self):
        filename = os.path.join('data/produce', '20-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'20/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'MAGUIÑA ROBLES, WILFREDO HERIBERTO')
        self.assertEqual(item.get('time_start'), u'09:08:34')
        self.assertEqual(item.get('institution'), u'produce')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'32824731')
        self.assertEqual(item.get('office'), u'DESPACHO VICEMINISTERIAL DE PESQUERIA')
        self.assertEqual(item.get('reason'), u'ENTREVISTA')
        self.assertEqual(item.get('host_name'), u'KASTNER URIBE, MONICA CARLOTA')
        self.assertEqual(item.get('time_end'), u'09:16:28')
        self.assertEqual(item.get('date'), u'2015-08-20')

        self.assertEqual(item.get('sha1'), u'1edbaca51007f25bd6bd07b0025bc94309544e3e')

        item = next(items)
        item = next(items)

        self.assertEqual(item.get('full_name'), u'REGALO QUIJANO, WALTER MANUEL')
        self.assertEqual(item.get('time_start'), u'09:16:39')
        self.assertEqual(item.get('institution'), u'produce')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'08182131')
        self.assertEqual(item.get('office'), u'DESPACHO VICEMINISTERIAL DE PESQUERIA')
        self.assertEqual(item.get('reason'), u'ENTREVISTA')
        self.assertEqual(item.get('host_name'), u'KASTNER URIBE, MONICA CARLOTA')
        self.assertEqual(item.get('time_end'), u'11:53:16')
        self.assertEqual(item.get('date'), u'2015-08-20')
        self.assertEqual(item.get('sha1'), u'd435683995c845a4a947895d3197725e255753ef')

        number_of_items = 1 + sum(1 for _ in items)

        self.assertEqual(number_of_items, 28)

    def test_correct_hash_sha1_for_legacy_data(self):
        item = {
            'full_name': u'LAVERIAN HERRERA, EFRAIN',
            'entity': '',
            'meeting_place': '',
            'office': u'OFICINA DE LOGISTICA',
            'host_name': u'URDANEGUI CABREJOS, FABRIZIO MARIO RAUL',
            'reason': u'DEJAR DOCUMENTO',
            'institution': u'produce',
            'location': '',
            'id_number': u'32613418',
            'id_document': u'DNI',
            'date': u'2008-01-02',
            'time_start': u'16:16:51',
            'time_end': u'17:15:31',
            'objective': '',
        }
        result = make_hash(item)
        expected = 'af716f0ed4aa8e3d3f4e1b05908c30f02f3e74fa'
        self.assertEqual(expected, result['sha1'])
