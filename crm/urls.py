from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customers/', views.customers_list, name='customers'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('tasks/', views.tasks_list, name='tasks'),
    path('tasks/<int:pk>/update/', views.update_task, name='update_task'),
    path('orders/', views.orders_list, name='orders'),
    path('orders/<int:pk>/status/', views.update_order_status, name='update_order_status'),
]
