from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose

import datetime

from scrapylib.processors import default_output_processor, clean_spaces, strip

def filter_date(date):
    if isinstance(date, datetime.datetime):
        return datetime.date.strftime(date, '%Y-%m-%d')

    return date


class ManoloItemLoader(ItemLoader):
    default_output_processor = default_output_processor
    default_input_processor = MapCompose(filter_date, strip, clean_spaces)