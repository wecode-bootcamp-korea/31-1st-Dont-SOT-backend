import json, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings


from users.models import User

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