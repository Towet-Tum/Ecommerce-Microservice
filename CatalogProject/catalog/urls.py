from django.urls import path 
from . views import (
    CategoryListCreateView, CategoryDetailView,
    ProductListCreateView, ProductDetailView,
)

urlpatterns = [
    # Categories endpoints
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Products endpoints
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    
]
