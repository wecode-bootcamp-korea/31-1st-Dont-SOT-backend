import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SOTJIMAYO.settings")
django.setup()

from products.models import AllergenStatus

CSV_ALLERGENSTATUSES    = 'products/csv_files/allergenstatuses.csv'

def allergenstatuses():
    with open(CSV_ALLERGENSTATUSES) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            AllergenStatus.objects.create(name = row[0])

allergenstatuses()
