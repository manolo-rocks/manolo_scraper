import os
import unittest

from manolo_scraper.spiders.presidencia import PresidenciaSpider
from utils import fake_response_from_file


# url: http://www.presidencia.gob.pe/visitas/index.php

class TestPresidenciaSpider(unittest.TestCase):

    def setUp(self):
        self.spider = PresidenciaSpider()

    def test_parse_item(self):
        filename = os.path.join('data/presidencia', '31-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'31/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'PAJARES CRIADO SERGIO ADOLFO')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'09272448')
        self.assertEqual(item.get('entity'), u'COSAPI DATA.S.A.')
        self.assertEqual(item.get('reason'), u'OTROS: PROYECTO DE CABLEADO (SUPERVISAR)')
        self.assertEqual(item.get('host_name'), u'CALDERON MONTOYA BLAS')
        self.assertEqual(item.get('office'), u'DIRECCION DE OPERACIONES')
        self.assertEqual(item.get('time_start'), u'19:04')
        self.assertEqual(item.get('time_end'), u'19:53')
        self.assertEqual(item.get('institution'), u'presidencia')
        self.assertEqual(item.get('meeting_place'), u'DESAMPARADOS')
        self.assertEqual(item.get('date'), u'2015-08-31')

        number_of_items = 1 + sum(1 for _ in items)

        self.assertEqual(number_of_items, 47)
