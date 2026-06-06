from django.contrib import admin
from .models import Customer, Interaction, Task


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'status', 'total_spent', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'phone', 'email']
    ordering = ['-created_at']


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'interaction_type', 'subject', 'created_at']
    list_filter = ['interaction_type']
    search_fields = ['customer__name', 'subject']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'priority', 'status', 'due_date', 'created_at']
    list_filter = ['priority', 'status']
    search_fields = ['title']
