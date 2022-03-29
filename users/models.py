from django.db import models

from products.models import Product, Option

class User(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name  = models.CharField(max_length = 30)
    username   = models.CharField(max_length = 30)
    password   = models.CharField(max_length = 200)
    email      = models.EmailField(unique = True, max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "users"



class Cart(models.Model):
    user     = models.ForeignKey("User", on_delete = CASCADE)
    product  = models.ForeignKey("products.Product", on_delete = CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = "carts"


class CartOption(models.Model):
    cart = models.ForeignKey("Cart", on_delete = CASCADE)
    option = models.ForeignKey("products.Option", on_delete = CASCADE)