# -*- coding: utf-8 -*-
from spiders import SireviSpider


class MincuSpider(SireviSpider):
    name = 'mincu'

    allowed_domains = ['visitas.mcultura.gob.pe']

    base_url = 'http://visitas.mcultura.gob.pe'

    institution_name = 'mincu'
