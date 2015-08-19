import os
import unittest

from manolo_scraper.spiders.minsa import MinsaSpider
from utils import fake_response_from_file


class TestMinsaSpider(unittest.TestCase):

    def setUp(self):
        self.spider = MinsaSpider()

    def test_parse_item(self):
        filename = os.path.join('data/minsa', '18-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'18/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'MELENDEZ ARISTA GREIDY')
        self.assertEqual(item.get('time_start'), u'18:45:09')
        self.assertEqual(item.get('institution'), u'minsa')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'41339966')
        self.assertEqual(item.get('entity'), u'DIRESA AMAZONAS')
        self.assertEqual(item.get('reason'), u'TRAMITE')
        self.assertEqual(item.get('host_name'), u'VELASQUEZ VALDIVIA ANIBAL')
        self.assertEqual(item.get('title'), u'MINISTRO DE SALUD')
        self.assertEqual(item.get('office'), u'DESPACHO MINISTERIAL')
        self.assertEqual(item.get('time_end'), None)
        self.assertEqual(item.get('date'), u'2015-08-18')

        number_of_items = 1 + sum(1 for x in items)

        self.assertEqual(number_of_items, 20)
