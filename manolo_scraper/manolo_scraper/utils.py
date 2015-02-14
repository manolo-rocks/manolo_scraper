from unidecode import unidecode
import hashlib
import re


def make_hash(item):
    hash_input = str(
        str(item['institution']) +
        str(unidecode(item['full_name'])) +
        str(unidecode(item['id_document'])) +
        str(unidecode(item['id_number'])) +
        str(item['date']) +
        str(unidecode(item['time_start']))
    )
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


def get_this_month(number):
    if number == '01':
        return 'enero'
    elif number == '02':
        return 'febrero'
    elif number == '03':
        return 'marzo'
    elif number == '04':
        return 'abril'
    elif number == '05':
        return 'mayo'
    elif number == '06':
        return 'junio'
    elif number == '07':
        return 'julio'
    elif number == '08':
        return 'agosto'
    elif number == '09':
        return 'setiembre'
    elif number == '10':
        return 'octubre'
    elif number == '11':
        return 'noviembre'
    elif number == '12':
        return 'diciembre'