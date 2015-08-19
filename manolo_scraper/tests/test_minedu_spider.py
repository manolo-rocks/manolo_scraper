# -*- coding: utf-8 -*-
import os
import unittest

from manolo_scraper.spiders.minedu import MineduSpider
from utils import fake_response_from_file


class TestMineduSpider(unittest.TestCase):

    def setUp(self):
        self.spider = MineduSpider()

    def test_parse_item(self):
        filename = os.path.join('data/minedu', '18-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'18/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'CARLOS MANUEL RIVERA BARDALES')
        self.assertEqual(item.get('time_start'), u'17:19')
        self.assertEqual(item.get('institution'), u'minedu')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'43531636')
        self.assertEqual(item.get('entity'), u'PARTICULAR')
        self.assertEqual(item.get('reason'), u'MOTIVO INSTITUCIONAL')
        self.assertEqual(item.get('host_name'), u'BERTHA ANGELA BANICH ALLEON')
        self.assertEqual(item.get('title'), u'[SECRETARIA / O IV]')
        self.assertEqual(item.get('office'), u'EDIFICIO L PISO 02')
        self.assertEqual(item.get('time_end'), None)
        self.assertEqual(item.get('date'), u'2015-08-18')

        number_of_items = 1 + sum(1 for x in items)
        self.assertEqual(number_of_items, 15)
