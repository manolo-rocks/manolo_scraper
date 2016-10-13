"""Save scraped items into our database"""
import datetime
import logging

from tqdm import tqdm
from hubstorage import HubstorageClient

from manolo_scraper.models import db_connect
from manolo_scraper.settings import API_KEY
from manolo_scraper.settings import SH_PROJECT


SPIDERS = [
    {
        "spider_name": "osce",
        "institution_name": "osce",
    },
    {
        "spider_name": "minagr",
        "institution_name": "minagr",
    },
    {
        "spider_name": "justicia",
        "institution_name": "justicia",
    }
]

def fetch_and_save_items():
    hc = HubstorageClient(auth=API_KEY)
    project = hc.get_project(SH_PROJECT)
    for spider in SPIDERS:
        print("\nworking on spider {}".format(spider['spider_name']))
        spider_id = project.ids.spider(spider['spider_name'])
        summary = project.spiders.lastjobsummary(spiderid=spider_id)
        for element in summary:
            print(element['key'])
            job = hc.get_job(element['key'])
            items = job.items.iter_values()
            save_items(items, spider['institution_name'])


def save_items(items, institution):
    print("processing {}".format(institution))
    db = db_connect()
    table = db['visitors_visitor']
    hashes_in_db = [i['sha1'] for i in table.find(institution=institution)]
    items_to_upload = []
    for item in tqdm(items):
        if item['sha1'] not in hashes_in_db:
            if '_type' in item:
                del item['_type']
            if '_key' in item:
                del item['_key']
            if 'title' not in item:
                item['title'] = ""
            if 'id_number' not in item:
                item['id_number'] = ""
            item['created'] = datetime.datetime.now()
            item['modified'] = datetime.datetime.now()
            item['date'] = datetime.datetime.strptime(item['date'], "%Y-%m-%d")
            items_to_upload.append(item)
            logging.info(
                "Saving: {0}, date: {1}".format(item['sha1'], item['date']))
        else:
            logging.info(
                "{0}, date: {1} is found in db, not saving".format(
                    item['sha1'],
                    item['date'],
                )
            )
    if items_to_upload:
        print("uploading {} items".format(len(items_to_upload)))
        table.insert_many(items_to_upload)
    else:
        print("nothing to upload to db")


def main():
    fetch_and_save_items()


if __name__ == "__main__":
    main()
