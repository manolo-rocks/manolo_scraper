#!/bin/bash

last_week=$(date --date='7 days ago' +"%Y-%m-%d")

cd /data2/ani/projects/aniversario_peru_github/manolo_scraper/manolo_scraper

tsocks /home/ani/.virtualenvs/manolo_scraper/bin/scrapy crawl inpe -a date_start=$last_week \
    > /home/ani/Desktop/log
