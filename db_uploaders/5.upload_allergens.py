import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SOTJIMAYO.settings")
django.setup()

from products.models import Allergen

CSV_ALLERGENS           = 'products/csv_files/allergens.csv'

def allergens():
    with open(CSV_ALLERGENS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            Allergen.objects.create(name = row[0])

allergens()