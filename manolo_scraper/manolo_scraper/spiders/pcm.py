# -*- coding: utf-8 -*-
from spiders import SireviSpider


class PcmSpider(SireviSpider):
    name = 'pcm'
    allowed_domains = ["hera.pcm.gob.pe"]

    base_url = 'http://hera.pcm.gob.pe/Visitas/controlVisitas'

    institution_name = 'pcm'
