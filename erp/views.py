from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

from erp.models import Brand, Category, Parfum, Order, Expense, Supplier, StockMovement


def inventory(request):
    parfums = Parfum.objects.select_related('brand').all()
    low_stock = parfums.filter(stock__lt=5)
    movements = StockMovement.objects.order_by('-created_at')[:20]
    return render(request, 'erp/inventory.html', {
        'parfums': parfums,
        'low_stock': low_stock,
        'movements': movements,
    })


def add_stock(request):
    if request.method == 'POST':
        parfum_id = request.POST.get('parfum_id')
        quantity = int(request.POST.get('quantity', 0))
        unit_price = request.POST.get('unit_price', 0)
        if parfum_id and quantity > 0:
            parfum = get_object_or_404(Parfum, pk=parfum_id)
            parfum.stock += quantity
            parfum.save()
            StockMovement.objects.create(
                parfum_name=str(parfum),
                movement_type='in',
                quantity=quantity,
                unit_price=unit_price,
            )
    return redirect('inventory')


def finances(request):
    if request.method == 'POST':
        Expense.objects.create(
            title=request.POST.get('title', ''),
            category=request.POST.get('category', 'other'),
            amount=request.POST.get('amount', 0),
            date=request.POST.get('date') or date.today(),
            description=request.POST.get('description', ''),
        )
        return redirect('finances')

    total_revenue = Order.objects.aggregate(s=Sum('total_amount'))['s'] or 0
    total_expenses = Expense.objects.aggregate(s=Sum('amount'))['s'] or 0
    return render(request, 'erp/finances.html', {
        'expenses': Expense.objects.all(),
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'profit': total_revenue - total_expenses,
    })


def suppliers(request):
    if request.method == 'POST':
        Supplier.objects.create(
            name=request.POST.get('name', ''),
            contact_person=request.POST.get('contact', ''),
            country=request.POST.get('country', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
        )
        return redirect('suppliers')
    return render(request, 'erp/suppliers.html', {'suppliers': Supplier.objects.all()})


def products_manage(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name', '').strip()
        category_name = request.POST.get('category_name', '').strip()
        brand, _ = Brand.objects.get_or_create(name=brand_name)
        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
        Parfum.objects.create(
            name=request.POST.get('name', ''),
            brand=brand,
            category=category,
            gender=request.POST.get('gender', 'unisex'),
            price=request.POST.get('price', 0),
            discount_price=request.POST.get('discount_price') or None,
            stock=int(request.POST.get('stock', 0)),
            size=request.POST.get('size', '100ml'),
            top_notes=request.POST.get('top_notes', ''),
            heart_notes=request.POST.get('heart_notes', ''),
            base_notes=request.POST.get('base_notes', ''),
            description=request.POST.get('description', ''),
            is_featured='is_featured' in request.POST,
            is_new='is_new' in request.POST,
        )
        return redirect('products_manage')
    return render(request, 'erp/products.html', {
        'parfums': Parfum.objects.select_related('brand', 'category').all(),
    })
