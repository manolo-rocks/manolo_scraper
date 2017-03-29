# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name='manolo',
    version='1.1',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = manolo_scraper.settings']},
    install_requires=['unipath', 'dataset'],
    package_data={'manolo_scraper': [
        'splash/*.lua',
    ]},
)
