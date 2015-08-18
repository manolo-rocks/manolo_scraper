#!-*- encoding: utf-8 -*-
import unittest

from manolo_scraper.utils import get_dni


class TestUtils(unittest.TestCase):
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
