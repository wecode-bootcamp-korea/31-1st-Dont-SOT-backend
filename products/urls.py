from django.urls import path

from products.views import ProductAllView

urlpatterns = [
    path('/all', ProductAllView.as_view()),
]