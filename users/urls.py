from django.urls import path
from .views import SignupView, IdcheckView, SignInView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/signup/idcheck', IdcheckView.as_view()),
    path('/signin', SignInView.as_view()),
]
