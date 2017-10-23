# -*- coding: utf-8 -*-

# Scrapy settings for manolo_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import yaml
import os
import sys

from unipath import Path


BASE_DIR = Path(__file__).absolute().ancestor(3)
SECRETS_FILE = os.path.join(BASE_DIR, 'config.yml')

if os.path.isfile(SECRETS_FILE):
    with open(SECRETS_FILE) as f:
        secrets = yaml.load(f.read())
else:
    secrets = {
        "SECRET_KEY": "",
        "POSTGRESQL_PASSWORD": "",
        "CRAWLERA_USER": "",
        "CRAWLERA_PASS": "",
        "drivername": "",
        "database": "",
        "username": "",
        "host": "",
        "password": "",
        "port": "",
        "api_key": "",
        "sh_project": "",
        "SPLASH_URL": "",
        "scraping_past_number_of_days": "",
        "banned_spiders": "",
    }


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable in settings".format(setting)
        print(error_msg)
        sys.exit(1)

CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 5

BOT_NAME = 'manolo_scraper'

SPIDER_MODULES = ['manolo_scraper.spiders']
NEWSPIDER_MODULE = 'manolo_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"
API_KEY = get_secret("api_key")
SH_PROJECT = get_secret("sh_project")

# scraping last X number of days
SCRAPING_PAST_NUMBER_OF_DAYS = get_secret("scraping_past_number_of_days")
CRAWLERA_ENABLED = False
CRAWLERA_USER = get_secret("CRAWLERA_USER")
CRAWLERA_PASS = get_secret("CRAWLERA_PASS")
BANNED_SPIDERS = get_secret("banned_spiders")

DOWNLOADER_MIDDLEWARES = {
    'scrapylib.crawlera.CrawleraMiddleware': 600,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'manolo_scraper.middlewares.ProxyMiddleware': 410,
}

LOG_LEVEL = 'DEBUG'
LOG_ENABLED = True

# also create a test_manolo for unittests
DATABASE = {
    'drivername': get_secret('drivername'),
    'database': get_secret('database'),
    'username': get_secret('username'),
    'host': get_secret('host'),
    'password': get_secret('password'),
    'port': get_secret('port'),
}

ITEM_PIPELINES = {
    'manolo_scraper.pipelines.DuplicatesPipeline': 300,
    'manolo_scraper.pipelines.CleanItemPipeline': 400,
}

DUPEFILTER_DEBUG = True
COOKIES_DEBUG = True
COOKIES_ENABLED = True

SPLASH_URL = 'http://{}:8050'.format(
    get_secret("SPLASH_URL"),
)
