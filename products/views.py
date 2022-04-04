import json

from rest_framework            import exceptions
from rest_framework.exceptions import ParseError

from django.views              import View
from django.http               import JsonResponse
from django.core               import serializers

from products.models           import Menu, Category, Product, RelativeProduct, ProductImage, Ingredient, Allergen, AllergenStatus, ProductAllergen

class ProductView(View):
    def get(self, request):
        menu     = request.GET.get('menu')
        category = request.GET.get('category')

        # try :
        if not menu or category in request.GET:
            raise exceptions.ParseError("NONE_MENU_OR_CATEGORY", 400)

        menus      = Menu.objects.filter(id=menu)
        categories = Category.objects.filter(id=category)
        products   = Product.objects.filter(category=categories[0])

        results = [
            {   
                "menu"     : [{
                    "id"   : menu.id,
                    "name" : menu.name,
                } for menu in menus],
                
                "category" : [{
                    "id"   : category.id, 
                    "name" : category.name,
                } for category in categories],

                "products" : [{
                    "id"    : product.id,
                    "name"  : product.name,
                    "image" : [product_image.image_url for product_image in ProductImage.objects.filter(product=product)],
                    "price" : int(product.price)
                } for product in products]
            }
        ]

        return JsonResponse({'results':results}, status=200)

        # except ParseError as error:
        #     return JsonResponse(
        #         'Invalid JSON - {0}'.format(error.detail),
        #         status=400
        #     )

        # except ParseError as e:
        #     return ({'message':(e.message)}, status=400)
                

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product             = Product.objects.get(id = product_id)
            product_option      = Product.objects.get(name='곱빼기')
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
                    'option'          : product_option.name,
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
