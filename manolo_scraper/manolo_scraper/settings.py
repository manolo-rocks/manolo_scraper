# -*- coding: utf-8 -*-

# Scrapy settings for manolo_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import json
import os
import sys

from unipath import Path


BASE_DIR = Path(__file__).absolute().ancestor(3)
SECRETS_FILE = os.path.join(BASE_DIR, 'config.json')

with open(SECRETS_FILE) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable in settings".format(setting)
        print(error_msg)
        sys.exit(1)

CONCURRENT_REQUESTS = 50
CONCURRENT_REQUESTS_PER_DOMAIN = 50
DOWNLOAD_DELAY = 10

BOT_NAME = 'manolo_scraper'

SPIDER_MODULES = ['manolo_scraper.spiders']
NEWSPIDER_MODULE = 'manolo_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'manolo_scraper (+http://www.yourdomain.com)'
CRAWLERA_ENABLED = False
CRAWLERA_USER = get_secret("CRAWLERA_USER")
CRAWLERA_PASS = get_secret("CRAWLERA_PASS")
DOWNLOADER_MIDDLEWARES = {
    'scrapylib.crawlera.CrawleraMiddleware': 600,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': "http://" + CRAWLERA_USER + ":" + CRAWLERA_PASS + "@proxy.crawlera.com:8010/",
}

LOG_LEVEL = 'DEBUG'
LOG_ENABLED = True

# also create a test_manolo for unittests
DATABASE = {
    'drivername': get_secret('drivername'),
    'database': get_secret('database'),
}

ITEM_PIPELINES = {
    'manolo_scraper.pipelines.DuplicatesPipeline': 300,
    'manolo_scraper.pipelines.CleanItemPipeline': 400,
}