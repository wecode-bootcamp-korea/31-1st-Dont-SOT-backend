from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length = 30)

    class Meta:
        db_table = "menus"


class Category(models.Model):
    name = models.CharField(max_length = 30)
    menu = models.ForeignKey("Menu", on_delete = models.CASCADE)

    class Meta:
        db_table = "categories"


class Product(models.Model): 
    name             = models.CharField(max_length = 30, null = True)
    price            = models.DecimalField(max_digits = 10, decimal_places = 2)
    description      = models.TextField()
    calory           = models.DecimalField(max_digits = 10, decimal_places = 2, null = True)
    category         = models.ForeignKey("Category", on_delete = models.SET_NULL, null = True)
    relative_product = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    sales            = models.IntegerField(default = 0)

    class Meta:
        db_table = "products"
        
class ProductImage(models.Model):
    image_url = models.URLField(max_length = 200)
    product   = models.ForeignKey("Product", on_delete = models.CASCADE)

    class Meta:
        db_table = "productimages"


class Ingredient(models.Model):
    name    = models.CharField(max_length = 30, null = True)
    made_in = models.CharField(max_length = 30, null = True)
    product = models.ForeignKey("Product", on_delete = models.CASCADE)

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


