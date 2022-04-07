import json

from django.views              import View
from django.http               import JsonResponse
from django.db.models          import Count

from products.models           import Menu, Category, Product, ProductImage, Ingredient, Allergen, AllergenStatus, ProductAllergen

class ProductView(View):
    def get(self, request):
        category = request.GET.get('category', '행사')
        sorting = request.GET.get('sorting', '-sales')
        limit    = int(request.GET.get('limit', 30))
        offset   = int(request.GET.get('offset', 0))

        try:
            if category:
                products   = Product.objects.filter(category__name = category, relative_product = None)[offset:offset+limit]

            products = Product.objects.filter(relative_product = None).order_by(sorting)[offset:offset+limit][:14]

            results = [
                {
                    "id"    : product.id,
                    "name"  : product.name,
                    "image" : [product_image.image_url for product_image in product.productimage_set.all()],
                    "price" : int(product.price)
                } for product in products]

            return JsonResponse({'results':results}, status=200)

        except ValueError:
            return JsonResponse({"message":'INVALID_VALUE'}, status = 400)


class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product             = Product.objects.get(id = product_id)
            product_images      = ProductImage.objects.filter(product=product.id)
            product_ingredients = Ingredient.objects.filter(product=product.id)
            allergens           = Allergen.objects.all()
            allergenlist = []

            for allergen in allergens:
                productallergen = ProductAllergen.objects.get(product = product.id, allergen = allergen.id)
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

            return JsonResponse({'message' : 'INVALID_PRODUCT'} , status = 401) 