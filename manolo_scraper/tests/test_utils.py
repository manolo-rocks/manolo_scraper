# -*- coding: utf-8 -*-
import unittest

from manolo_scraper.utils import get_dni
from manolo_scraper.utils import get_this_month
from manolo_scraper.utils import make_hash


class TestGetDNI(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_dni_from_numbers(self):
        given = '47174595'
        expected = 'DNI', '47174595'
        result = get_dni(given)
        self.assertEqual(expected, result)

    def test_get_dni_from_dni_and_number(self):
        given = 'DNI 08675405'
        expected = 'DNI', '08675405'
        result = get_dni(given)
        self.assertEqual(expected, result)

    def test_get_dni_from_cedula_and_number(self):
        given = 'CEDULA DIPLOMATICA DE IDENTIDAD CS469187'
        expected = 'CEDULA DIPLOMATICA DE IDENTIDAD', 'CS469187'
        result = get_dni(given)
        self.assertEqual(expected, result)

    def test_get_dmi_documento_militar_de_indentidad(self):
        given = 'DMI : 803802300'
        expected = 'DMI', '803802300'
        result = get_dni(given)
        self.assertEqual(expected, result)

    def test_get_dmi_with_dash(self):
        given = 'DMI : O-95505'
        expected = 'DMI', 'O-95505'
        result = get_dni(given)
        self.assertEqual(expected, result)

    def test_get_otr(self):
        given = 'OTR : 0196307704'
        expected = 'OTR', '0196307704'
        result = get_dni(given)
        self.assertEqual(expected, result)

    def test_get_cex(self):
        given = 'CEX : 1478-2011'
        expected = 'CEX', '1478-2011'
        result = get_dni(given)
        self.assertEqual(expected, result)

    def test_get_cdi(self):
        given = 'CDI : EA814654'
        expected = 'CDI', 'EA814654'
        result = get_dni(given)
        self.assertEqual(expected, result)

    def test_get_passport(self):
        given = 'PSP : AI0386093'
        expected = 'PSP', 'AI0386093'
        result = get_dni(given)
        self.assertEqual(expected, result)

    def test_get_brevete(self):
        given = 'ATG : BREVETE'
        expected = 'ATG', 'BREVETE'
        result = get_dni(given)
        self.assertEqual(expected, result)


class TestMakeHash(unittest.TestCase):
    def setUp(self):
        pass

    def test_hash_using_complete_data(self):
        item = {
            'date': '2015-08-11',
            'entity': u'SCOTIANK BANCK',
            'full_name': u'DOMINGUEZ OCAÑA, SANDRA BEATRIZ',
            'host_name': u'AGUADO ALFARO, JOSE ALBERTO',
            'id_document': u'DNI/LE',
            'id_number': u'10153798',
            'institution': u'congreso',
            'location': '',
            'meeting_place': '',
            'office': u'ADMINISTRACION LUIS ALBERTO SANCHEZ - FERNANDO BELAUNDE TERRY',
            'reason': u'MANTENIMIENTO PROGRAMADO',
            'time_end': u'15:06',
            'time_start': u'09:04',
            'title': u'ADMINISTRADOR DE EDIFICIOS',
        }
        result = make_hash(item)
        expected = '4784d22af48c79154d69b4dd4c1562b8f3a7d182'
        self.assertEqual(expected, result['sha1'])

    def test_hash_missing_id_number(self):
        item = {
            'date': '2015-08-11',
            'entity': u'SCOTIANK BANCK',
            'full_name': u'DOMINGUEZ OCAÑA, SANDRA BEATRIZ',
            'host_name': u'AGUADO ALFARO, JOSE ALBERTO',
            'id_document': u'DNI/LE',
            'institution': u'congreso',
            'location': '',
            'meeting_place': '',
            'office': u'ADMINISTRACION LUIS ALBERTO SANCHEZ - FERNANDO BELAUNDE TERRY',
            'reason': u'MANTENIMIENTO PROGRAMADO',
            'time_end': u'15:06',
            'time_start': u'09:04',
            'title': u'ADMINISTRADOR DE EDIFICIOS',
        }
        result = make_hash(item)
        expected = 'daf54933e2164e0c2da44ea0fc2b66dce011ecc1'
        self.assertEqual(expected, result['sha1'])


class TestGetThisMonth(unittest.TestCase):
    def test_diciembre(self):
        expected = 'diciembre'
        result = get_this_month('12')
        self.assertEqual(expected, result)
