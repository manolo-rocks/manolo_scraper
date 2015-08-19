# -*- coding: utf-8 -*-

import os
import unittest

from manolo_scraper.spiders.minem import MinemSpider
from utils import fake_response_from_file


class TestMinemSpider(unittest.TestCase):

    def setUp(self):
        self.spider = MinemSpider()

    def test_parse_item(self):
        filename = os.path.join('data/minem', '19-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'19/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'CARMEN ALICIA GUTIERREZ VELASCO')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'08241251')
        self.assertEqual(item.get('entity'), u'ESLOM')
        self.assertEqual(item.get('reason'), u'REUNI\xc3\u201cN DE TRABAJO')
        self.assertEqual(item.get('host_name'), u'OMAR FRANCO CHAMBERGO RODRIGUEZ')
        self.assertEqual(item.get('office'), u'DIRECCION GENERAL DE HIDROCARBUROS-N')
        self.assertEqual(item.get('time_start'), u'08:01')
        self.assertEqual(item.get('time_end'), u'08:17')
        self.assertEqual(item.get('meeting_place'), u'OFICINA DEL FUNCIONARIO')
        self.assertEqual(item.get('institution'), u'minem')
        self.assertEqual(item.get('date'), u'2015-08-19')

        number_of_items = 1 + sum(1 for _ in items)

        self.assertEqual(number_of_items, 20)
