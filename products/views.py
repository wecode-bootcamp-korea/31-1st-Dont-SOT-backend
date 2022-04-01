from django.views    import View
from django.http     import JsonResponse

from products.models import Menu, Category, Product, RelativeProduct, ProductImage, Ingredient, Allergen, AllergenStatus, ProductAllergen

class ProductAllView(View):
    def get(self, request):
       
        category_id = request.GET.get('category_id')

        if category_id == None:
            menus      = Menu.objects.all()
            categories = Category.objects.all()
            products   = Product.objects.all()

            results = [{
                "id"       : menu.id,
                "name"     : menu.name,
                "category" : [{
                    "id"      : category.id,
                    "name"    : category.name,
                    "product" : [{
                        "id"    : product.id,
                        "name"  : product.name,
                        "image" : [product_image.image_url for product_image in ProductImage.objects.filter(product=product)],
                        "price" : product.price
                    } for product in Product.objects.filter(category=category)]
                } for category in Category.objects.filter(menu=menu)]
            } for menu in menus]

            return JsonResponse({'results':results}, status=200)

        else:
            categories = Category.objects.filter(id=category_id)
            products = Product.objects.filter(category=categories[0])
        
            results = [
                {   
                    "category" : [{
                        "id"   : category.id, 
                        "name" : category.name,
                    } for category in categories],

                    "products" : [{
                        "id"    : product.id,
                        "name"  : product.name,
                        "image" : [product_image.image_url for product_image in ProductImage.objects.filter(product=product)],
                        "price" : product.price
                    } for product in products]
                }
            ]

            return JsonResponse({'results':results}, status=200)
        

        # results = [{
        #     "id"       : menu.id,
        #     "name"     : menu.name,
        #     "category" : [{
        #         "id"      : category.id,
        #         "name"    : category.name,
        #         "product" : [{
        #             "id"    : product.id,
        #             "name"  : product.name,
        #             "image" : [product_image.image_url for product_image in ProductImage.objects.filter(product=product)],
        #             "price" : product.price
        #         } for product in Product.objects.filter(category=category)]
        #     } for category in Category.objects.filter(menu=menu)]
        # } for menu in menus]

        # return JsonResponse({'results':results}, status=200)

        # results = [{
        #     "name" : product.name,
        #     ""
        # } for product in products]

        # results = [{
        #     "name"  : owner.name,
        #     "email" : owner.email,
        #     "age"   : owner.age,
        #     "dogs"  : [{
        #         "name" : dog.name,
        #         "age"  : dog.age
        #     } for dog in owner.dog_set.all()]
        # } for owner in owners]
        

        # products = Product.objects.all()
        
        # for menu in menus:
        #     for category in categoryies:
        #         for product in products:
        #             menu_id
        #             category_id
        #             product_id = product.id
        #             product_name = product.name
        #             product_images = Image.objects.filter(product = product)
        #             product_price = product.price
        #         ["id" : menu_id, "category" : menu_category , "categoryList" :
        #         ["id" : , "miniCategory" : , "contents":
        #         [{“id”: 1,
        #             “menuName”: “두입 족발 도시락“,
        #             “images”: “/images/fooditem.jpg”,
        #             “price”: “5,800"} for product in products] for category in categories]
        #             for menu in menus]


        # :8000/products?category_id=10[]
        # :8000/products?category_id=15
        # :8000/products?category_id=100

         # product = request.GET.get('product_id')
        # for i in category_id:
        #     category = Category.objects.get(category.id=i)
        # categories = Category.objects.filter(id=category_id)
        # products = Product.objects.filter(category=categories[0])   
        # products = Product.objects.filter(id=categories.name)
        # product  = Product.objects.get(id=product_id)
        # images   = ProductImage.objects.filter(product_id=product.id)