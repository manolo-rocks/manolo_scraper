import os
import unittest

from manolo_scraper.spiders.ambiente import AmbienteSpider
from utils import fake_response_from_file


# http://visitas.minam.gob.pe/frmConsulta.aspx
class TestAmbienteSpider(unittest.TestCase):

    def setUp(self):
        self.spider = AmbienteSpider()

    def test_parse_item(self):
        filename = os.path.join('data/ambiente', '19-08-2015.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'08/19/2015'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'PATRICIA ITURREGUI BYRNE')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'07231335')
        self.assertEqual(item.get('entity'), u'PERSONAL')
        self.assertEqual(item.get('reason'), u'OTROS')
        self.assertEqual(item.get('host_name'), u'RUPERTO ANDRES TABOADA DELGADO')
        self.assertEqual(item.get('office'), u'POR DEFINIR')
        self.assertEqual(item.get('meeting_place'), u'POR DEFINIR')
        self.assertEqual(item.get('time_start'), u'04:01:20 p.m.')
        self.assertEqual(item.get('time_end'), u'09:07:00 a.m.')
        self.assertEqual(item.get('institution'), u'ambiente')
        self.assertEqual(item.get('date'), u'2015-08-19')
        number_of_items = 1 + sum(1 for _ in items)
        self.assertEqual(number_of_items, 15)

    def test_parse_item_2(self):
        filename = os.path.join('data/ambiente', '06-02-2017.html')
        items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'02/06/2017'}))

        item = next(items)
        self.assertEqual(item.get('full_name'), u'Carolina Margarita Bocanegra Gamboa de Marquina')
        self.assertEqual(item.get('id_document'), u'DNI')
        self.assertEqual(item.get('id_number'), u'41724666')
        self.assertEqual(item.get('entity'), u'AFP INTEGRA')
        self.assertEqual(item.get('reason'), u'REUNI\xd3N DE TRABAJO')
        self.assertEqual(item.get('host_name'), u'ROSEMARIE REBECA AVILA BOSQUEANGOSTO')
        self.assertEqual(item.get('office'), u'POR DEFINIR')
        self.assertEqual(item.get('meeting_place'), u'POR DEFINIR')
        self.assertEqual(item.get('time_start'), u'05:47:37 p.m.')
        self.assertEqual(item.get('time_end'), u'06:53:23 p.m.')
        self.assertEqual(item.get('institution'), u'ambiente')
        self.assertEqual(item.get('date'), u'2017-02-06')
        number_of_items = 1 + sum(1 for _ in items)
        self.assertEqual(number_of_items, 15)

