from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/add-stock/', views.add_stock, name='add_stock'),
    path('finances/', views.finances, name='finances'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('products/', views.products_manage, name='products_manage'),
]
