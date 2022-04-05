import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError
from django.conf  import settings


from users.models      import User
from users.validations import validate_username, validate_email, validate_password

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
        
        try:
            data           = json.loads(request.body)
            product_id     = data['product_id']
            qunatity       = data['quantity']
            sizeup         = data['sizeup']
            sizeup_product = Product.objects.get(relative_product_id = product_id)

            if sizeup_product==None:
                return JsonResponse({"message" : "SIZEUP_INVALID"}, status = 401)

            if sizeup:
                product = Product.objects.get(relative_product_id = product_id)
            
            cart, created = Cart.objects.get_or_create(user = request.user, product_id = product.id)
            cart.quantity = quantity
            
            return JsonResponse({"message" : "SUCCESS"},  status = 200)

        except KeyError:
            return JsonResponse({"messgae" : "KEY_ERROR"}, status = 401)


    @SignInDecorator
    def patch(self, request):
        
        data       = json.loads(request.body)
        product_id = data['product_id']
        qunatity   = data['quantity']
        sizeup     = data['sizeup']

        if sizeup:
            product = Product.objects.get(relative_product_id = product_id)

        cart = Cart.objects.get(user = request.user, product = product.id)
        
        if quantity==0:
            cart.delete()
            return JsonResponse({"message" : "PRODUCT_DELETED_FROM_CART"} , status = 204)
    
        if quantity < 0:
            return JsonResponse({"message" : "INVALID_QUANTITY"}, status = 401)
        
        cart.quantity = quantity
        return JsonResponse({"message" : "SUCCESS"}, status = 200)


    
    @SignInDecorator
    def get(self, request):
        carts = Cart.objects.filter(user = request.user)
        results = []
        for cart in carts:
            product = cart.product
            option = False
            if product.relative_product:
                option = True
                product = product.relative_product 
            results += [{
                "product_id" : product.id,
                "price" : product.price,
                "option" : option ,
                "quantity" : cart.quantity
            }]
        return JsonResponse({"results" : results}, status = 200)


    @SignInDecorator
    def delete(self, request):
        
        data       = json.loads(request.body)
        product_id = data['product_id']
        sizeup     = data['sizeup']
        user       = request.user

        if sizeup:
            product_id = Product.objects.get(relative_product_id = product_id).id

        cart = Cart.objects.get(user = user, product_id = product_id)

        if cart == None:
            return JsonResponse({"message" : "INVALID_REQUEST"}, status = 401)

        cart.delete()
        return JsonResponse({"message" : "SUCCESS"}, status = 204)

