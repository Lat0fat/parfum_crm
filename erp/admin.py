from django.contrib import admin
from .models import Brand, Category, Parfum, Order, Supplier, Warehouse, StockMovement, Expense


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Parfum)
class ParfumAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'gender', 'price', 'stock', 'is_featured', 'is_new']
    list_filter = ['brand', 'category', 'gender', 'is_featured', 'is_new']
    search_fields = ['name', 'brand__name']
    ordering = ['-created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'total_amount', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['customer_name', 'customer_phone']
    ordering = ['-created_at']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'country', 'created_at']
    search_fields = ['name', 'contact_person', 'phone']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'manager']
    search_fields = ['name', 'manager']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['parfum_name', 'movement_type', 'quantity', 'unit_price', 'supplier', 'created_at']
    list_filter = ['movement_type', 'supplier']
    search_fields = ['parfum_name']
    ordering = ['-created_at']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'amount', 'date', 'created_at']
    list_filter = ['category']
    search_fields = ['title']
    ordering = ['-date']
