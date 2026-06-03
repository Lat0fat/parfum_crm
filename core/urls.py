from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Shop
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('parfum/<int:pk>/', views.parfum_detail, name='parfum_detail'),
    path('checkout/', views.checkout, name='checkout'),
    # CRM/ERP Dashboard
    path('panel/', views.dashboard, name='dashboard'),
    path('panel/customers/', views.customers_list, name='customers'),
    path('panel/customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('panel/tasks/', views.tasks_list, name='tasks'),
    path('panel/tasks/<int:pk>/update/', views.update_task, name='update_task'),
    path('panel/orders/', views.orders_list, name='orders'),
    path('panel/orders/<int:pk>/status/', views.update_order_status, name='update_order_status'),
    # ERP
    path('panel/inventory/', views.inventory, name='inventory'),
    path('panel/inventory/add-stock/', views.add_stock, name='add_stock'),
    path('panel/finances/', views.finances, name='finances'),
    path('panel/suppliers/', views.suppliers, name='suppliers'),
    path('panel/products/', views.products_manage, name='products_manage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
