# -*- coding: utf-8 -*-
from spiders import SireviSpider


class MinagrSpider(SireviSpider):
    name = 'minagr'

    allowed_domains = ['minagri.gob.pe']

    base_url = 'http://visitas.minagri.gob.pe/visitas/controlVisitas'

    institution_name = 'minagr'
