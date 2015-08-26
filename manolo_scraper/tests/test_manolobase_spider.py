import unittest

from scrapy import exceptions

from manolo_scraper.spiders.spiders import ManoloBaseSpider


class TestManoloBaseSpider(unittest.TestCase):

    def test_start_date_and_end_date(self):
        with self.assertRaises(exceptions.UsageError):
            ManoloBaseSpider(date_start='2015-08-20', date_end='2015-08-17', name='manolo')