import json
import re
import time
from calendar import Calendar
from datetime import datetime, timedelta
import hashlib

from unidecode import unidecode
from botasaurus import browser, AntiDetectDriver
from selenium.webdriver.common.by import By
from parsel import Selector


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
INSTITUTIONS = [
    ("20492966658", "ambiente"),
    ("20131370645", "mef"),
    ("20131371617", "minjus"),
    ("20545565359", "midis"),
    ("20131372931", "minagr"),
    ("20504774288", "mincetur"),
    ("20131370998", "minedu"),
    ("20131368829", "minem"),
    ("20504743307", "vivienda"),
    ("20131379944", "mtc"),
    ("20336951527", "min. mujer"),
    ("20168999926", "pcm"),
    ("20504794637", "produce"),
    ("20131023414", "trabajo"),
    ("20537630222", "mincu"),
    ("20419026809", "osce"),
    ("20100152356", "sedapal"),
    ("20131312955", "sunat"),
    ("20131380951", "municipalidad de lima"),
    ("20131367938", "defensa"),
]


def make_hash(item):
    hash_input = ''
    hash_input += str(item['institution'])

    if 'full_name' in item:
        hash_input += str(unidecode(item['full_name']))

    if 'id_document' in item:
        hash_input += str(unidecode(item['id_document']))

    if 'id_number' in item:
        hash_input += str(unidecode(item['id_number']))

    hash_input += str(item['date'])

    if 'time_start' in item:
        hash_input += str(unidecode(item['time_start']))

    hash_output = hashlib.sha1()
    hash_output.update(hash_input.encode("utf-8"))
    item['sha1'] = hash_output.hexdigest()
    return item


def get_dni(document_identity):
    id_document = ''
    id_number = ''

    document_identity = document_identity.replace(':', ' ')
    document_identity = re.sub('\s+', ' ', document_identity)
    document_identity = document_identity.strip()
    document_identity = re.sub('^', ' ', document_identity)

    res = re.search("(.*)\s(([A-Za-z0-9]+\W*)+)$", document_identity)
    if res:
        id_document = res.groups()[0].strip()
        id_number = res.groups()[1].strip()

    if id_document == '':
        id_document = 'DNI'

    return id_document, id_number


@browser(
    headless=True,
    user_agent=USER_AGENT,
)
def scrape(driver: AntiDetectDriver, data):
    institution_id, institution_name = data
    url = "https://visitas.servicios.gob.pe/consultas/"
    driver.get(url)
    time.sleep(2)

    all_months = []
    start_date = datetime(2023, 10, 1)
    end_date = datetime.now()

    scraped_elements = []

    current_date = start_date
    while current_date <= end_date:
        date_tuple = (current_date.year, current_date.month)
        if date_tuple not in all_months:
            all_months.append(date_tuple)
        current_date += timedelta(days=30)  # Assuming each month has 30 days for simplicity

    # fill form element 3
    input_element = driver.find_element(By.ID, "txtbuscar")
    input_element.send_keys(institution_id)

    for month_item in all_months:
        year, month = month_item
        start_day = datetime(year, month, 1)
        calendar = Calendar()
        for item in calendar.itermonthdays(year, month):
            if item != 0:
                end_day = datetime(year, month, item)

        date_range = f"{start_day.strftime('%d/%m/%Y')} - {end_day.strftime('%d/%m/%Y')}"

        # fill form element 1
        driver.execute_script(
            f"document.getElementById('fechabus').setAttribute('value', '{date_range}')"
        )

        # fill form element 2
        date_range_button = driver.find_element(By.CLASS_NAME, "buscar_web2")
        driver.execute_script(
            f'arguments[0].innerHTML = "{date_range}";',
            date_range_button
        )

        # do search
        search_button = driver.find_element(By.ID, "buscar")
        search_button.click()
        time.sleep(15)

        while True:
            time.sleep(1)
            sel = Selector(driver.page_source)
            rows = sel.xpath('//table[@id="maintable"]//tr')
            for row in rows:
                item = row.xpath('td/text()').extract()

                if len(item) > 9:
                    id_document, id_number = get_dni(item[4])
                    split_item = item[6].split(" - ")
                    host_name = split_item[0]
                    office = split_item[1]
                    host_title = " - ".join(split_item[2:])

                    scraped_element = {
                        "full_name": item[3],
                        "entity": item[5],
                        "id_number": id_number,
                        "id_document": id_document,
                        "host_name": host_name,
                        "office": office,
                        "host_title": host_title,
                        "reason": item[9],
                        "meeting_place": item[10],
                        "institution": institution_name,
                        "time_start": item[7],
                        "time_end": item[8],
                        "location": "",
                        "date": datetime.strptime(item[1], '%d/%m/%Y').strftime('%Y-%m-%d'),
                    }
                    if scraped_element not in scraped_elements:
                        scraped_elements.append(scraped_element)
                        with open("scraped_elements.jl", "a") as handle:
                            handle.write(json.dumps(scraped_element) + "\n")

            next_button = driver.find_element(By.ID, "maintable_next")
            if "disabled" in next_button.get_attribute("class"):
                break
            print("Elements scraped:", len(scraped_elements))
            next_button.click()

    return scraped_elements


if __name__ == "__main__":
    scrape(INSTITUTIONS)
