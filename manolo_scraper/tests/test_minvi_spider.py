# -*- coding: utf-8 -*-
import os
import unittest

from manolo_scraper.spiders.minvi import MinviSpider
from utils import fake_response_from_file


class TestMinviSpider(unittest.TestCase):

    def setUp(self):
        self.spider = MinviSpider()

    def test_parse_item(self):
        filename = os.path.join('data/minvi', '18-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'18/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'CESAR MAMANI ROMERO')
        self.assertEqual(item.get('time_start'), u'18:07')
        self.assertEqual(item.get('institution'), u'vivienda')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'10157944')
        self.assertEqual(item.get('entity'), u'TRABAJADOR - PARH')
        self.assertEqual(item.get('reason'), u'REUNI\xc3\u201cN DE TRABAJO')
        self.assertEqual(item.get('host_name'), u'DAYANA FARRO .')
        self.assertEqual(item.get('title'), u'P.A.H.R. [OTROS]')
        self.assertEqual(item.get('office'), u'PNT')
        self.assertEqual(item.get('time_end'), None)
        self.assertEqual(item.get('date'), u'2015-08-18')

        number_of_items = 1 + sum(1 for x in items)
        self.assertEqual(number_of_items, 15)
