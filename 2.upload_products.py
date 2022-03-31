import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SOTJIMAYO.settings")
django.setup()

from products.models import Product, Category, RelativeProduct

CSV_PRODUCTS            = 'products/csv_files/products.csv'
CSV_RELATIVE_PRODUCTS   = 'products/csv_files/relative_products.csv'

def products():

    with open(CSV_PRODUCTS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            category_name = row[4]
            category_id   = Category.objects.get(name = category_name).id

            Product.objects.create(name = row[0], price = row[1], description = row[2], calory = row[3], category_id = category_id)

    with open(CSV_RELATIVE_PRODUCTS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            product          = Product.objects.get(name = row[0])
            relative_product = Product.objects.get(name = row[1])

            RelativeProduct.objects.create(product = product ,relative_product = relative_product)

products()