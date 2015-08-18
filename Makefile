test:
	nosetests -v -w manolo_scraper

coverage:
	rm -rf manolo_scraper/cover
	rm -rf .coverage
	nosetests -v -w manolo_scraper --cover-package=manolo_scraper --cover-html --with-coverage --cover-inclusive
