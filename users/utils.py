import json, jwt

from django.conf  import settings
from django.http  import JsonResponse

from users.models import User

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get('Authorization', None)
            payload      = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)           
    return wrapper