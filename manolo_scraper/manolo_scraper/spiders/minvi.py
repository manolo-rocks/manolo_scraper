# -*- coding: utf-8 -*-
from spiders import SireviSpider


class MinviSpider(SireviSpider):
    name = 'minvi'

    allowed_domains = ['geo.vivienda.gob.pe']

    base_url = 'http://geo.vivienda.gob.pe/Visitas/controlVisitas'

    institution_name = 'vivienda'
