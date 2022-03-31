from django.urls import path, include
from .views import SignupView, IdcheckView

urlpatterns = {
    path('/signup', SignupView.as_view()),
    path('/signup/idcheck', IdcheckView.as_view())
}