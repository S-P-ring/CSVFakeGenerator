import csv
from faker import Faker
import random

import uuid

from .models import DataSchema


def prepare_data(object: DataSchema) -> List[str]:
    """Accepts a model object and returns a list of column names"""
    fields = {}
    for column in object.column_set.all():
        if column.data_type in ('TEXT', 'INTEGER'):
            fields[column.name] = {'data_type': column.data_type, 'order': column.order,
                                   'range_min': column.range_min,
                                   'range_max': column.range_max}
        else:
            fields[column.name] = {'data_type': column.data_type, 'order': column.order}
    return fields


def generate_filename(extension: str) -> str:
    unique_filename = str(uuid.uuid4())
    return f"{unique_filename}.{extension}"


def generate_data(data_type: str, range_min: int, range_max: int) -> str | int:
    fake = Faker()
    if data_type == 'TEXT':
        return fake.paragraph(nb_sentences=random.randint(range_min, range_max))
    elif data_type == 'INTEGER':
        return random.randint(range_min, range_max)
    elif data_type == 'FULL_NAME':
        return fake.name()
    elif data_type == 'JOB':
        return fake.job()
    elif data_type == 'EMAIL':
        return fake.email()
    elif data_type == 'DOMAIN_NAME':
        return fake.domain_name()
    elif data_type == 'PHONE_NUMBER':
        return fake.phone_number()
    elif data_type == 'COMPANY_NAME':
        return fake.company()
    elif data_type == 'ADDRESS':
        return fake.address()
    elif data_type == 'DATE':
        return fake.date()
    else:
        return None


def generate_row(field_dict:dict) -> List[str]:
    row_data = []
    for field_name in sorted(field_dict.keys(), key=lambda x: field_dict[x]['order']):
        field_data = field_dict[field_name]
        if 'data_type' in field_data:
            data_type = field_data['data_type']
            range_min = field_data.get('range_min', 0)
            range_max = field_data.get('range_max', 0)
            row_data.append(generate_data(data_type, range_min, range_max))
        else:
            row_data.append('')
    return row_data


def generate_csv(field_dict: dict, num_rows: int, column_separator: str, string_character: str) -> None:
    filename = generate_filename('csv')
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=column_separator, quotechar=string_character)
        header_row = []
        for field_name in sorted(field_dict.keys(), key=lambda x: field_dict[x]['order']):
            header_row.append(field_name)
        writer.writerow(header_row)
        for i in range(num_rows):
            row_data = generate_row(field_dict)
            writer.writerow(row_data)
