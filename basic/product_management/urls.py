# myapp/urls.py
from django.urls import path
from .views import ProductCreateView, ProductListView, ProductDetailView, PurchaseCreateView, PurchaseListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('purchases/', PurchaseListView.as_view(), name='purchase-list'),
    path('purchases/create/', PurchaseCreateView.as_view(), name='purchase-create'),
]
