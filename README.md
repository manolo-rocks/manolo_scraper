# All spiders go here
Spiders are based on [Scrapy](https://github.com/scrapy/scrapy).

# Configuration
Create a file `config.json` with the following info:

```javascript
{
    "CRAWLERA_USER": "",
    "CRAWLERA_PASS": "",
    "drivername": "postgres",
    "username": "postgres",
    "host": "localhost",
    "port": "5432",
    "password": "",
    "database": "manolo"
}
```

The database credentials are needed so that the spider will upload data to the
production database.

