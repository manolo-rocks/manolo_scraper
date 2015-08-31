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
        self.assertEqual(item.get('full_name'), u'RICCE CHUMBE WALTER HUMBERTO')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'25424360')
        self.assertEqual(item.get('entity'), u'MINISTERIO DE AMBIENTE')
        self.assertEqual(item.get('reason'), u'REUNION DE TRABAJO')
        self.assertEqual(item.get('host_name'), u'MONTALVA DE FALLA JOSE')
        self.assertEqual(item.get('office'), u'SUBSECRETARIA GENERAL')
        self.assertEqual(item.get('title'), u'DIRECTOR GENERAL')
        self.assertEqual(item.get('time_start'), u'10:50')
        self.assertEqual(item.get('time_end'), u'10:54')
        self.assertEqual(item.get('institution'), u'presidencia')
        self.assertEqual(item.get('meeting_place'), u'EDIFICIO PALACIO')
        self.assertEqual(item.get('date'), u'2015-08-31')

        number_of_items = 1 + sum(1 for _ in items)

        self.assertEqual(number_of_items, 12)
