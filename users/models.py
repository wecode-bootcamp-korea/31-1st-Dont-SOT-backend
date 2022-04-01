from django.db import models

from products.models import Product

class User(models.Model):
    name       = models.CharField(max_length = 30)
    username   = models.CharField(unique = True, max_length = 30)
    password   = models.CharField(max_length = 200)
    email      = models.EmailField(unique = True, max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "users"



class Cart(models.Model):
    user     = models.ForeignKey("User", on_delete = models.CASCADE)
    product  = models.ForeignKey("products.Product", on_delete = models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = "carts"

