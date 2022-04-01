from django.views    import View
from django.http     import JsonResponse

from products.models import Menu, Category, Product, RelativeProduct, ProductImage, Ingredient, Allergen, AllergenStatus, ProductAllergen

class ProductAllView(View):
    def get(self, request):
        
