import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SOTJIMAYO.settings")
django.setup()

from products.models import Menu, Category

CSV_MENUCATEGORIES      = 'products/csv_files/menucategories.csv'

def insert_menucategories():

    with open(CSV_MENUCATEGORIES) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            if row[0]:
                menu_name = row[0]
                Menu.objects.create(name = menu_name)

            category_name = row[1]

            menu_id = Menu.objects.get(name = menu_name).id

            Category.objects.create(name = category_name, menu_id = menu_id)

insert_menucategories()