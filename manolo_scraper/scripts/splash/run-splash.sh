#!/usr/bin/env bash
echo 'Splash is running on http://127.0.0.1:8050'
docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash