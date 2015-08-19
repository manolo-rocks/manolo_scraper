# -*- coding: utf-8 -*-
from spiders import SireviSpider


class OSCESpider(SireviSpider):
    name = "osce"

    allowed_domains = ['visitas.osce.gob.pe']

    base_url = 'http://visitas.osce.gob.pe/controlVisitas'
    institution_name = 'osce'
