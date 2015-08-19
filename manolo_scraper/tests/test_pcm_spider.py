# -*- coding: utf-8 -*-
import os
import unittest

from manolo_scraper.spiders.pcm import PcmSpider
from utils import fake_response_from_file


class TestPcmSpider(unittest.TestCase):

    def setUp(self):
        self.spider = PcmSpider()

    def test_parse_item(self):
        filename = os.path.join('data/pcm', '18-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'18/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('date'), u'2015-08-18')
        self.assertEqual(item.get('full_name'), u'CUEVA FRANCISCO GUERRA GARCIA')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'09179830')
        self.assertEqual(item.get('entity'), u'COMISION DINI')
        self.assertEqual(item.get('reason'), u'MOTIVO INSTITUCIONAL')
        self.assertEqual(item.get('location'), u'PALACIO')
        self.assertEqual(item.get('host_name'), u'Pedro Cateriano Bellido')
        self.assertEqual(item.get('office'), u'DESPACHO MINISTERIAL [PRESIDENTE DEL CONSEJO DE MINISTROS]')
        self.assertEqual(item.get('meeting_place'), u'SALA TELLO')
        self.assertEqual(item.get('time_start'), u'19:00')
        self.assertEqual(item.get('time_end'), u'19:40')
        self.assertEqual(item.get('institution'), u'pcm')

        number_of_items = 1 + sum(1 for x in items)
        self.assertEqual(number_of_items, 15)
