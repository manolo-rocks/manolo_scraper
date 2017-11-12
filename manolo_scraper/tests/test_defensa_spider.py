# -*- coding: utf-8 -*-
import os
import unittest

from manolo_scraper.spiders.defensa import DefensaSpider
from manolo_scraper.utils import make_hash
from utils import fake_response_from_file


class TestMineduSpider(unittest.TestCase):

    def setUp(self):
        self.spider = DefensaSpider()

    def test_parse_item(self):
        filename = os.path.join('data/defensa', '19-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'19/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'HORTENCIA VANESSA GONZALES VALDIVIA')
        self.assertEqual(item.get('time_start'), u'08:48')
        self.assertEqual(item.get('institution'), u'defensa')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'41795231')
        self.assertEqual(item.get('entity'), u'CONIDA')
        self.assertEqual(item.get('reason'), u'REUNION DE TRABAJO')
        self.assertEqual(item.get('host_name'), u'DUPEYRAT LUQUE WOLFGANG CARLOS DOUGLAS')
        self.assertEqual(item.get('time_end'), u'09:49')
        self.assertEqual(item.get('date'), u'08/11/2017')
        self.assertEqual(item.get('sha1'), u'd7d3fc2a9a0f123473817b201dac7e651aee445a')

        item = next(items)
        self.assertEqual(item.get('full_name'), u'RIGOBERTO SALAS ASENCIOS')
        self.assertEqual(item.get('institution'), u'defensa')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'43847220')
        self.assertEqual(item.get('entity'), u'AGENCIA DE COMPRAS DE LAS FF. AA.')
        self.assertEqual(item.get('reason'), u'REUNION DE TRABAJO')
        self.assertEqual(item.get('host_name'), u'DUPEYRAT LUQUE WOLFGANG CARLOS DOUGLAS')
        self.assertEqual(item.get('time_start'), u'09:00')
        self.assertEqual(item.get('time_end'), u'12:35')
        self.assertEqual(item.get('date'), u'08/11/2017')
        self.assertEqual(item.get('sha1'), u'eb0ba95644a1e97f93d2ca8332ecece7007627f2')

        number_of_items = sum(1 for _ in items)
        self.assertEqual(number_of_items, 8)

    def test_correct_hash_sha1_for_legacy_data(self):
        item = {
            'date': '2013-10-24',
            'entity': u'',
            'full_name': u'JUAN PONCE VILLARROEL',
            'host_name': u'FERNANDO NOBLECILLA ZUÑIGA',
            'id_document': u'DNI',
            'id_number': u'08882615',
            'institution': u'defensa',
            'location': '',
            'meeting_place': '',
            'office': u'',
            'reason': u'VISITA PERSONAL',
            'time_start': u'17:28',
            'time_end': u'18:00',
            'title': u'',
        }
        result = make_hash(item)
        expected = 'dd3e23e4a1b146e250f759666bd0cfdcf0c3db8d'
        self.assertEqual(expected, result['sha1'])
