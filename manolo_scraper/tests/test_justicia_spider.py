import os
import unittest

from manolo_scraper.spiders.justicia import JusticiaSpider
from utils import fake_response_from_file


# url: http://app3.minjus.gob.pe:8080/visita_web/consulta_visita_comision

class TestJusticiaSpider(unittest.TestCase):

    def setUp(self):
        self.spider = JusticiaSpider()

    def test_parse_item(self):
        filename = os.path.join('data/justicia', '27-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'27/08/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'CERON GUTIERREZ, NANCY')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'07862529')
        self.assertEqual(item.get('entity'), u'PARTICULAR')
        self.assertEqual(item.get('reason'), u'CONSULTA DE EXPEDIENTE DEL REGISTRO UNICO DE VICTIMAS')
        self.assertEqual(item.get('host_name'), u'SOTO PEREZ, ADRIEL EDUARDO')
        self.assertEqual(item.get('office'), u'CONSEJO DE REPARACIONES')
        # self.assertEqual(item.get('meeting_place'), u'POR DEFINIR')
        self.assertEqual(item.get('time_start'), u'10:12')
        self.assertEqual(item.get('time_end'), u'11:12')
        self.assertEqual(item.get('institution'), u'minjus')
        self.assertEqual(item.get('location'), u'CONSEJO DE REPARACIONES - SECRETARIA TECNICA, NEISER LLACZA ARCE 158, MIRAFLORES')
        self.assertEqual(item.get('date'), u'2015-08-27')

        number_of_items = 1 + sum(1 for _ in items)

        self.assertEqual(number_of_items, 30)
