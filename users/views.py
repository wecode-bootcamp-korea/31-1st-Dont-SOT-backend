import json, re, bcrypt, jwt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError
from django.conf            import settings
from django.db.models       import Case, When

from products.models   import Menu, Category, Product, ProductImage
from users.models      import User, Cart
from users.validations import validate_username, validate_email, validate_password
from users.utils       import signin_decorator

class IdcheckView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            username = data['username']

            validate_username(username)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"message" : "REGISTERED_USERNAME"}, status = 401) 

            return JsonResponse({"message" : "CHECK_SUCCESS"}, status = 200)

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
            return JsonResponse({'message':'INVALID_USER'}, status = 401)


class CartView(View):    
    @signin_decorator
    def post(self, request):
        
        try:
            data         = json.loads(request.body)
            product_name = data['product_name']
            sizeup       = data['sizeup']

            if sizeup and not Product.objects.filter(relative_product__name = product_name).exists():            
                return JsonResponse({'message': 'SIZEUP_INVALID'}, status = 406)

            product = Product.objects.get(relative_product__name = product_name)

            cart, created = Cart.objects.get_or_create(user = request.user, product_id = product.id, defaults={'quantity': 1})
            
            if not created:
                cart.quantity += 1
                cart.save()
                return JsonResponse({"message" : "UPDATED"}, status = 200)
            
            return JsonResponse({"message" : "CART_CREATED"},  status = 201)

        except KeyError:
            return JsonResponse({"messgae" : "KEY_ERROR"}, status = 400)


    @signin_decorator
    def patch(self, request, cart_id):
        try:
            data       = json.loads(request.body)
            quantity   = data['quantity']
 
            Cart.objects.filter(id=cart_id).update(quantity = quantity)

            return JsonResponse({"message" : "SUCCESS"}, status = 200)

        except KeyError:
            return JsonResponse({"messgae" : "KEY_ERROR"}, status = 400)
    

    @signin_decorator
    def get(self, request):
        carts = Cart.objects.filter(user = request.user).annotate(
            has_relative_product = Case(When(product__isnull=True, then=False), default=True)
            )

        if not carts.exists():
            return JsonResponse({"message" : "INVALID_REQUEST"}, status = 400)

        results = [{
            "cart_id"     : cart.id,
            "price"       : int(cart.product.price),
            "sizeup"      : cart.has_relative_product,
            "quantity"    : cart.quantity,
            "image"       : cart.product.productimage_set.first().image_url,
            "product_name": cart.product.name
        } for cart in carts]

        return JsonResponse({"results" : results}, status = 200)


    @signin_decorator
    def delete(self, request, cart_id):
        try:
            Cart.objects.get(id = cart_id).delete()

        except Cart.DoesNotExist:
            return JsonResponse({"message" : "INVALID_REQUEST"}, status = 400)

        return JsonResponse({"message" : "DELETE_SUCCESS"}, status = 204)

