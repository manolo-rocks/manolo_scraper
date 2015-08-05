# -*- coding: utf-8 -*-
from spiders import SireviSpider


class MinagrSpider(SireviSpider):
    name = 'minagr'

    allowed_domains = ['sistemas.minag.gob.pe']

    base_url = 'http://sistemas.minag.gob.pe/visitas/controlVisitas'

    institution_name = 'minagr'
