import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SOTJIMAYO.settings")
django.setup()

from products.models import Ingredient

CSV_PRODUCT_INGREDIENTS = 'products/csv_files/product_ingredients.csv'

def product_ingredients():

    with open(CSV_PRODUCT_INGREDIENTS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            if row[0]:
                product_name = row[0]

                product      = Product.objects.get(name = product_name)

            Ingredient.objects.create(product = product, name = row[1], made_in = row[2])

product_ingredients()