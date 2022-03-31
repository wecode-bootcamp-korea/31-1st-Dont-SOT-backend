import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SOTJIMAYO.settings")
django.setup()

from products.models import Allergen, AllergenStatus, Product, ProductAllergen

CSV_PRODUCT_ALLERGENS   = 'products/csv_files/product_allergens.csv'

def productallergens():
    with open(CSV_PRODUCT_ALLERGENS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            if row[0]:
                product_name = row[0]
                product      = Product.objects.get(name = product_name)
            allergen = Allergen.objects.get(name = row[1])
            status = AllergenStatus.objects.get(name = row[2])

            ProductAllergen.objects.create(product = product, allergen = allergen, status = status)

productallergens()