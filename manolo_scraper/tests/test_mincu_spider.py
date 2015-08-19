# -*- coding: utf-8 -*-
import os
import unittest

from manolo_scraper.spiders.mincu import MincuSpider
from utils import fake_response_from_file


class TestMincuSpider(unittest.TestCase):

    def setUp(self):
        self.spider = MincuSpider()

    def test_parse_item(self):
        filename = os.path.join('data/mincu', '18-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'18/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'INGRID BARRIONUEVO ECHEGARAY')
        self.assertEqual(item.get('time_start'), u'16:40')
        self.assertEqual(item.get('institution'), u'mincu')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'10085172')
        self.assertEqual(item.get('entity'), u'PARTICULAR')
        self.assertEqual(item.get('reason'), u'REUNIÃ“N DE TRABAJO')
        self.assertEqual(item.get('host_name'), u'JOIZ ELIZABETH DOBLADILLO ORTIZ')
        self.assertEqual(item.get('title'), u'[SERVICIOS DE UN ASISTENTE EN COMUNICACIONES]')
        self.assertEqual(item.get('office'), u'QHAPAQ Ã‘AN')
        self.assertEqual(item.get('time_end'), u'16:53')
        self.assertEqual(item.get('date'), u'2015-08-18')

        number_of_items = 1 + sum(1 for x in items)
        self.assertEqual(number_of_items, 15)
