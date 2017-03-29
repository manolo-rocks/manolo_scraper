#!/usr/bin/env bash
echo 'Splash Jupyter is running on http://127.0.0.1:8888'
docker run -p 8888:8888 -v $(PWD)/notebooks:/notebooks -it scrapinghub/splash-jupyter