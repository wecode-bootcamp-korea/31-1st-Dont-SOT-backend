import json

from django.views              import View
from django.http               import JsonResponse

from products.models           import Menu, Category, Product, RelativeProduct, ProductImage, Ingredient, Allergen, AllergenStatus, ProductAllergen

class ProductView(View):
    def get(self, request):
        category = request.GET.get('category', None)
        print(category)
        print(request.GET) # QueryDict

        limit    = int(request.GET.get('limit', 30))
        print(type(limit))
        offset   = int(request.GET.get('offset', 0))

        if category:
            products = Product.objects.filter(category__name = category)

        products = Product.objects.all()[offset:offset+limit]

        results = [
            {
                "products" : [{
                    "id"    : product.id,
                    "name"  : product.name,
                    "image" : [product_image.image_url for product_image in ProductImage.objects.filter(product=product)],
                    "price" : int(product.price)
                } for product in products]
            }
        ]

        return JsonResponse({'results':results}, status=200)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product             = Product.objects.get(id = product_id)
            product_images      = ProductImage.objects.filter(product=product.id)
            product_ingredients = Ingredient.objects.filter(product=product.id)
            allergens           = Allergen.objects.all()

            allergenlist = []

            for allergen in allergens:
                productallergen = ProductAllergen.objects.filter(product = product.id, allergen = allergen.id)[0]
                allergenstatus  = AllergenStatus.objects.get(id = productallergen.status.id)
                allergenlist += [{
                    'id'              : allergen.id,
                    'allergen_name'   : allergen.name,
                    'status'          : allergenstatus.name
                }]

            results = {
                    'image'           : [product_image.image_url for product_image in product_images],
                    'name'            : product.name,
                    'description'     : product.description,
                    'price'           : int(product.price),
                    'calory'          : product.calory,
                    'allergen'        : allergenlist,
                    'ingredient'      : [{
                            'id'         : product_ingredient.id,
                            'name'       : product_ingredient.name,
                            'made_in'    : product_ingredient.made_in
                        } for product_ingredient in product_ingredients],
            }
            return JsonResponse({'results' : results} , status = 200)

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_PRODUCT_ID'} , status = 404)
