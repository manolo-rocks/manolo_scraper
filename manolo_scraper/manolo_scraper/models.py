import dataset

from manolo_scraper import settings


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance

    :param test: if test is True then create an empty test database
    """
    database_name = settings.DATABASE['database']

    database = [
        settings.DATABASE['drivername'],
        '//' + settings.DATABASE['username'],
        settings.DATABASE['password'] + '@' + settings.DATABASE['host'],
        str(settings.DATABASE['port']) + '/' + database_name,
    ]
    url = ':'.join(database)

    db = dataset.connect(url)
    return db
