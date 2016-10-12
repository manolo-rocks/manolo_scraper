"""Save scraped items into our database"""
import datetime
import json
import logging
import sys

from tqdm import tqdm

from manolo_scraper.models import db_connect


def save_items(data):
    institution = data[0]['institution']
    db = db_connect()
    table = db['visitors_visitor']
    hashes_in_db = [i['sha1'] for i in table.find(institution=institution)]
    items_to_upload = []
    for item in tqdm(data):
        if item['sha1'] not in hashes_in_db:
            if '_type' in item:
                del item['_type']
            if 'title' not in item:
                item['title'] = ""
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
    with open(sys.argv[1].strip(), "r") as handle:
        data = [json.loads(i) for i in handle.readlines()]
    save_items(data)


if __name__ == "__main__":
    main()
