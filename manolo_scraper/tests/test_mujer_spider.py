# -*- coding: utf-8 -*-
import os
import unittest

from manolo_scraper.spiders.mujer import MujerSpider
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

        number_of_items = 1 + sum(1 for x in items)
        self.assertEqual(number_of_items, 20)
