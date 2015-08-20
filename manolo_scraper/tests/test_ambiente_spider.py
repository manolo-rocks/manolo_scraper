# import os
# import unittest
#
# from manolo_scraper.spiders.ambiente import AmbienteSpider
# from utils import fake_response_from_file
#
# # http://visitas.minam.gob.pe/frmConsulta.aspx
#
# class TestAmbienteSpider(unittest.TestCase):
#
#     def setUp(self):
#         self.spider = AmbienteSpider()
#
#     def test_parse_item(self):
#         filename = os.path.join('data/ambiente', '19-08-2015.html')
#         items = self.spider.parse(fake_response_from_file(filename, meta={'date': u'19/08/2015'}))
#
#         item = next(items)
#         self.assertEqual(item.get('full_name'), u'MIGUEL MOISES ASMAT LINARES')
#         self.assertEqual(item.get('id_document'), u'DNI/LE')
#         self.assertEqual(item.get('id_number'), u'47501611')
#         self.assertEqual(item.get('entity'), u'EL ROCOTO')
#         self.assertEqual(item.get('reason'), u'PERSONAL DEL CONCESIONARIO')
#         self.assertEqual(item.get('host_name'), u'PEREYRA SALAZAR, WALTER')
#         self.assertEqual(item.get('office'), u'G.F. DE SERVICIO SOCIAL')
#         self.assertEqual(item.get('time_start'), u'10:27:38 a.m')
#         self.assertEqual(item.get('time_end'), None)
#         self.assertEqual(item.get('institution'), u'congreso')
#         self.assertEqual(item.get('title'), u'TECNICO ADMINISTRATIVO')
#         self.assertEqual(item.get('date'), u'2015-08-19')
#
#         number_of_items = 1 + sum(1 for x in items)
#
#         self.assertEqual(number_of_items, 10)
