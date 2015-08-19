import os
import unittest

from manolo_scraper.spiders.minagr import MinagrSpider
from utils import fake_response_from_file


class TestMinagrSpider(unittest.TestCase):

    def setUp(self):
        self.spider = MinagrSpider()

    def test_parse_item(self):
        filename = os.path.join('data/minagr', '18-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'18/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'VICTOR HUGO SEVERINO VALLE')
        self.assertEqual(item.get('time_start'), u'17:04')
        self.assertEqual(item.get('institution'), u'minagr')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'25856019')
        self.assertEqual(item.get('entity'), u'MAKA SAC')
        self.assertEqual(item.get('reason'), u'DOCUMENTOS')
        self.assertEqual(item.get('host_name'), u'CARLOS ANTONIO LARA PALACIOS')
        self.assertEqual(item.get('title'), u'[CONTADOR P\xc3\u0161BLICO PARA ALMAC\xc3\u2030N Y PATRIMONIO]')
        self.assertEqual(item.get('office'), u'ALMACEN CENTRAL')
        self.assertEqual(item.get('time_end'), u'17:23')
        self.assertEqual(item.get('date'), u'2015-08-18')

        number_of_items = 1 + sum(1 for x in items)
        self.assertEqual(number_of_items, 15)
