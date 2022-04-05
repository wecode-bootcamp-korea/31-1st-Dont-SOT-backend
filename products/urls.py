from django.urls import path
from products.views import ProductView, ProductDetailView, ProductBestView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/sort', ProductBestView.as_view()),
]