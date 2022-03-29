from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length = 30)

    class Meta:
        db_table = "menus"


class Category(models.Model):
    name = models.CharField(max_length = 30)
    menu = modles.ForeignKey("Menu", on_delete = models.CASCADE)

    class Meta:
        db_table = "categories"


class Product(models.Model):
    price            = models.DecimalField(max_digits = 10, decimal_places = 2)
    description      = models.TextField()
    calory           = models.DecimalField(max_digits = 10, decimal_places = 2)
    category         = models.ForeignKey("Category", on_delete = models.CASCADE)
    relative_product = models.ManyToManyField("self", through = "RelativeProduct", symmetrical = False)

    class Meta:
        db_table = "products"

class RelativeProduct(models.Model):
    name             = models.CharField(max_length = 30)
    product          = models.ForeignKey("Product", on_delete = models.CASCADE, related_name = "MainProduct")
    relative_product = models.ForeignKey("Product", on_delete = models.CASCADE, related_name = "OptionalProduct")

    class Meta:
        db_table = "relativeproducts"


class ProductImage(models.Model):
    image_url = modles.UrlField(max_length = 200)
    product   = modles.ForeignKey("Product", on_delete = models.CASCADE)

    class Meta:
        db_table = "productimages"


class Ingredient(models.Model):
    name    = models.CharField(max_length = 30)
    made_in = modles.CharField(max_length = 30)
    product = modles.ForeignKey("Product", on_delete = models.CASCADE)

    class Meta:
        db_table = "ingredients"


class Allergen(models.Model):
    name = models.CharField(max_length = 30)

    class Meta:
        db_table = "allergens"


class AllergenStatus(models.Model):
    name = models.CharField(max_length = 30)

    class Meta:
        db_table = "allergenstatuses"


class ProductAllergen(models.Model):
    product  = models.ForeignKey("Product", on_delete = models.CASCADE)
    allergen = models.ForeignKey("Allergen", on_delete = models.CASCADE)
    status   = models.ForeignKey("AllergenStatus", on_delete = models.CASCADE)

    class Meta:
        db_table = "product_allergens"


