from django.urls import path
from products.views import ProductView, ProductDetailView, ProductSortView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/sort', ProductSortView.as_view()),
]