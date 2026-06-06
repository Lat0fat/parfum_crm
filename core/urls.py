from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import crm.views as crm_views
import erp.views as erp_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # CRM
    path('', crm_views.dashboard, name='dashboard'),
    path('customers/', crm_views.customers_list, name='customers'),
    path('customers/<int:pk>/', crm_views.customer_detail, name='customer_detail'),
    path('tasks/', crm_views.tasks_list, name='tasks'),
    path('tasks/<int:pk>/update/', crm_views.update_task, name='update_task'),
    path('orders/', crm_views.orders_list, name='orders'),
    path('orders/<int:pk>/status/', crm_views.update_order_status, name='update_order_status'),

    # ERP
    path('inventory/', erp_views.inventory, name='inventory'),
    path('inventory/add-stock/', erp_views.add_stock, name='add_stock'),
    path('finances/', erp_views.finances, name='finances'),
    path('suppliers/', erp_views.suppliers, name='suppliers'),
    path('products/', erp_views.products_manage, name='products_manage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
