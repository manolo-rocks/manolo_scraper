#!/bin/bash

last_weeks=$(date --date='14 days ago' +"%Y-%m-%d")
today=$(date +"%Y-%m-%d")

# edit these path
spider=$1
scrapy_path=/home/yoni/manolo_scraper/manolo_scraper
scrapy_bin=/home/yoni/.virtualenvs/manolo_scraper/bin/scrapy
scraper_log=/home/yoni/manolo_scraper_logs.txt

cd $scrapy_path

# run using the name of the spider as argument
$scrapy_bin crawl $spider -a date_start=$last_weeks -a date_end=$today  \
      -o $1.jl >> $scraper_log 2>&1
