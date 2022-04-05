import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError
from django.conf  import settings


from users.models      import User, Cart
from users.validations import validate_username, validate_email, validate_password

# 127.0.0.1:8000/products/1

class IdcheckView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            username = data['username']

            validate_username(username)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"message" : "REGISTERED_USERNAME"}, status = 401) 

            return JsonResponse({"message" : "SUCCESS"}, status = 200)

        except ValidationError as e:
            return JsonResponse({"message" : e.message}, status = 401)


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name     = data['name']
            email    = data['email']
            password = data['password']
            username = data['username']
        
            validate_username(username)
            validate_password(password)
            validate_email(email)


            if User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "REGISTERED_EMAIL"}, status = 401)

            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name     = name,
                email    = email,
                password = hashed_password,
                username = username
            )
            return JsonResponse({"message" : 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except ValidationError as e:
            return JsonResponse({"message" : e.message}, status = 401)


class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['username']
            password = data['password']
            user     = User.objects.get(username = username)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            
            token = jwt.encode({'id':user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            
            return JsonResponse({'token':token}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

class CartView(View):
    @SignInDecorator
    def post(self, request):
        data           = json.loads(request.body)

        product_id     = data['product_id']
        quantity       = data['quantity']
        option         = data['option']

        sizeup_product = RelativeProduct.objects.get(relative_product = product_id)

        if not sizeup_product:
            return({"message" : "SIZEUP_INVALID"}, status = 401)

        if option and sizeup_product:
            product_id = RelativeProduct.objects.get(relative_product = product_id).product
         
        cart, created = Cart.objects.get_or_create(
            user       = request.user,
            product_id = product_id,
            defaults = {
                quantity : quantity
            }
        )

        if not created:
            cart.quantity = quantity

        return JsonResponse({"message" : "SUCCESS"}, status=200)

        # except KeyError:
        #     return ({"messgae" : KEY_ERROR}, status = 401)

    @SignInDecorator
    def patch(self, request)
        
        data = json.loads(request.body)
        product_id = data['product_id']
        qunatity = data['quantity']
        option = data['option']

        user = request.user

        if option:
            product_id = RelativeProduct.objects.get(relative_product = product_id).product

        cart = Cart.objects.get(product = product_id)
        
        if quantity==0:
            cart.delete()
            return ({"message" : "PRODUCT_DELETED_FORM_CART", status = 204})
    
        if quantity < 0:
            return ({"message" : "INVALID_QUANTITY", status = 401})
        
        cart.quantity = quantity
        return ({"message" : "SUCCESS", status = 200})


        
    #detail page
    # @SignInDecorator
    # def get(self, request):
    #     user = request.user
    #     items = Cart.objects.filter(user = user)
    #         for item in items:
    #             if Product.objects.get(item.product)
    #             product = Product.objects.get(product)
    #             result = 
    #             {
    #                 'product_id' : item.product
    #                 'product_images' : [ for image in Product.objects.filter(product.id = item.product)]
    #                 'produ'
    #             }

    @SignInDecorator
    def delete(self, request):
        
        data = json.loads(request.body)
        product_id = data['product_id']
        option = data['option']
        user = request.user

       if option:
            product_id = RelativeProduct.objects.get(relative_product = product_id).product

        cart = Cart.objects.get(user = user.id, product = product_id)

        if not cart:
            return({"message" : "INVALID_REQUEST"}, status = 401)

        cart.delete()
        return ({"message" : "SUCCESS", status = 204})

