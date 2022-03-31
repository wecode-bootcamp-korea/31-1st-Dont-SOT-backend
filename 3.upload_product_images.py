import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SOTJIMAYO.settings")
django.setup()

from products.models import Product, ProductImage

CSV_PRODUCT_IMAGES      = 'products/csv_files/product_images.csv'

def product_images():

    with open(CSV_PRODUCT_IMAGES) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            product = Product.objects.get(name = row[0])

            ProductImage.objects.create(product = product, image_url = row[1])

product_images()
