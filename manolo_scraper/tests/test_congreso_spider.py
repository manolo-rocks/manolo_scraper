import os
import unittest

from manolo_scraper.spiders.congreso import CongresoSpider
from utils import fake_response_from_file


class TestCongresoSpider(unittest.TestCase):

    def setUp(self):
        self.spider = CongresoSpider()

    def test_parse_item(self):
        filename = os.path.join('data/congreso', '18-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'18/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'ZEVALLOS FLOREZ, CESAR')
        self.assertEqual(item.get('time_start'), u'08:15')
        self.assertEqual(item.get('institution'), u'congreso')
        self.assertEqual(item.get('id_document'), u'DNI/LE')
        self.assertEqual(item.get('id_number'), u'07632139')
        self.assertEqual(item.get('entity'), u'EL ROCOTO')
        self.assertEqual(item.get('reason'), u'PERSONAL DEL CONCESIONARIO')
        self.assertEqual(item.get('host_name'), u'PEREYRA SALAZAR, WALTER')
        self.assertEqual(item.get('title'), u'TECNICO ADMINISTRATIVO')
        self.assertEqual(item.get('office'), u'G.F. DE SERVICIO SOCIAL')
        self.assertEqual(item.get('time_end'), None)
        self.assertEqual(item.get('date'), u'2015-08-18')

        number_of_items = 1

        for item in items:
            number_of_items += 1

        self.assertEqual(number_of_items, 10)
