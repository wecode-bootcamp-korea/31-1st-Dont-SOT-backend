import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SOTJIMAYO.settings")
django.setup()

from products.models import Menu, Category, Product, RelativeProduct, ProductImage, Ingredient, Allergen, AllergenStatus, ProductAllergen

CSV_PRODUCTS            = 'products/product.csv'
CSV_ALLERGENS           = 'products/allergens.csv'
CSV_ALLERGENSTATUSES    = 'products/allergenstatuses.csv'
CSV_MENUCATEGORIES      = 'products/menucategories.csv'
CSV_ALLERGENS           = 'products/allergens.csv'
CSV_PRODUCT_IMAGES      = 'products/product_images.csv'
CSV_PRODUCT_INGREDIENTS = 'products/product_ingredients.csv'
CSV_PRODUCTS            = 'products/products.csv'
CSV_RELATIVE_PRODUCTS   = 'products/relative_products.csv'
CSV_PRODUCT_ALLERGENS   = 'products/product_allergens.csv'


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

def product_images():

    with open(CSV_PRODUCT_IMAGES) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            product = Product.objects.get(name = row[0])

            ProductImage.objects.create(product = product, image_url = row[1])

product_images()

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

def allergens():
    with open(CSV_ALLERGENS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            Allergen.objects.create(name = row[0])

allergens()

def allergenstatuses():
    with open(CSV_ALLERGENSTATUSES) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            AllergenStatus.objects.create(name = row[0])

allergenstatuses()

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