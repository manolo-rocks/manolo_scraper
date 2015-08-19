# -*- coding: utf-8 -*-
import os
import unittest

from manolo_scraper.spiders.osce import OSCESpider
from utils import fake_response_from_file


class TestOsceSpider(unittest.TestCase):

    def setUp(self):
        self.spider = OSCESpider()

    def test_parse_item(self):
        filename = os.path.join('data/osce', '18-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'18/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'Silvia Sousa Cristofol')
        self.assertEqual(item.get('time_start'), u'16:38')
        self.assertEqual(item.get('institution'), u'osce')
        self.assertEqual(item.get('id_document'), u'CARNET DE EXTRANJERIA')
        self.assertEqual(item.get('id_number'), u'000904735')
        self.assertEqual(item.get('entity'), u'everis')
        self.assertEqual(item.get('reason'), u'REUNIÃ“N DE TRABAJO')
        self.assertEqual(item.get('host_name'), u'Isabel Rosario Vega Palomino')
        self.assertEqual(item.get('title'), u'[Ninguno]')
        self.assertEqual(item.get('office'), u'Sala de Espera')
        self.assertEqual(item.get('time_end'), None)
        self.assertEqual(item.get('date'), u'2015-08-18')

        number_of_items = 1 + sum(1 for x in items)
        self.assertEqual(number_of_items, 15)
