from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from django.contrib import messages
from .models import Parfum, Category, Brand, Order, OrderItem
from crm.models import Customer, Task, Interaction
from erp.models import StockMovement, Expense, Supplier
import json
from datetime import date, timedelta

def home(request):
    featured = Parfum.objects.filter(is_featured=True)[:8]
    new_arrivals = Parfum.objects.filter(is_new=True).order_by('-created_at')[:6]
    categories = Category.objects.all()
    brands = Brand.objects.all()[:10]
    context = {
        'featured': featured,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'shop/home.html', context)

def catalog(request):
    parfums = Parfum.objects.all()
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    gender = request.GET.get('gender')
    search = request.GET.get('q')
    sort = request.GET.get('sort', 'newest')

    if category_id:
        parfums = parfums.filter(category_id=category_id)
    if brand_id:
        parfums = parfums.filter(brand_id=brand_id)
    if gender:
        parfums = parfums.filter(gender=gender)
    if search:
        parfums = parfums.filter(Q(name__icontains=search) | Q(brand__name__icontains=search))

    if sort == 'price_asc':
        parfums = parfums.order_by('price')
    elif sort == 'price_desc':
        parfums = parfums.order_by('-price')
    elif sort == 'popular':
        parfums = parfums.order_by('-sold_count')
    else:
        parfums = parfums.order_by('-created_at')

    context = {
        'parfums': parfums,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
        'current_category': category_id,
        'current_brand': brand_id,
        'current_gender': gender,
        'search': search,
        'sort': sort,
    }
    return render(request, 'shop/catalog.html', context)

def parfum_detail(request, pk):
    parfum = get_object_or_404(Parfum, pk=pk)
    related = Parfum.objects.filter(category=parfum.category).exclude(pk=pk)[:4]
    return render(request, 'shop/detail.html', {'parfum': parfum, 'related': related})

def checkout(request):
    if request.method == 'POST':
        data = request.POST
        order = Order.objects.create(
            customer_name=data.get('name'),
            customer_phone=data.get('phone'),
            customer_email=data.get('email', ''),
            address=data.get('address'),
        )
        cart = json.loads(data.get('cart', '[]'))
        total = 0
        for item in cart:
            try:
                parfum = Parfum.objects.get(pk=item['id'])
                price = float(parfum.final_price)
                qty = int(item['qty'])
                OrderItem.objects.create(order=order, parfum=parfum, quantity=qty, price=price)
                total += price * qty
                parfum.sold_count += qty
                parfum.save()
            except:
                pass
        order.total_amount = total
        order.save()

        # Auto-create or update CRM customer
        customer, created = Customer.objects.get_or_create(
            phone=order.customer_phone,
            defaults={'name': order.customer_name, 'email': order.customer_email}
        )
        customer.total_spent += total
        if customer.total_spent > 5000000:
            customer.status = 'vip'
        elif customer.total_spent > 1000000:
            customer.status = 'active'
        customer.save()

        Interaction.objects.create(
            customer=customer,
            interaction_type='order',
            subject=f"Buyurtma #{order.pk} - {total:,.0f} so'm"
        )

        messages.success(request, f"Buyurtmangiz #{order.pk} qabul qilindi!")
        return JsonResponse({'success': True, 'order_id': order.pk})
    return render(request, 'shop/checkout.html')

# ─── ADMIN / CRM / ERP VIEWS ───────────────────────────────────────

def dashboard(request):
    today = date.today()
    month_start = today.replace(day=1)

    total_orders = Order.objects.count()
    month_orders = Order.objects.filter(created_at__date__gte=month_start).count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(s=Sum('total_amount'))['s'] or 0
    month_revenue = Order.objects.filter(status='delivered', created_at__date__gte=month_start).aggregate(s=Sum('total_amount'))['s'] or 0
    total_customers = Customer.objects.count()
    new_customers = Customer.objects.filter(created_at__date__gte=month_start).count()
    low_stock = Parfum.objects.filter(stock__lt=5).count()
    pending_orders = Order.objects.filter(status='new').count()
    tasks_due = Task.objects.filter(status__in=['todo', 'inprogress']).count()
    recent_orders = Order.objects.all()[:8]
    top_parfums = Parfum.objects.order_by('-sold_count')[:5]

    context = {
        'total_orders': total_orders, 'month_orders': month_orders,
        'total_revenue': total_revenue, 'month_revenue': month_revenue,
        'total_customers': total_customers, 'new_customers': new_customers,
        'low_stock': low_stock, 'pending_orders': pending_orders,
        'tasks_due': tasks_due, 'recent_orders': recent_orders,
        'top_parfums': top_parfums,
    }
    return render(request, 'crm/dashboard.html', context)

def customers_list(request):
    customers = Customer.objects.all()
    search = request.GET.get('q')
    status = request.GET.get('status')
    if search:
        customers = customers.filter(Q(name__icontains=search) | Q(phone__icontains=search))
    if status:
        customers = customers.filter(status=status)
    return render(request, 'crm/customers.html', {'customers': customers, 'status': status})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    interactions = customer.interactions.all()[:20]
    orders = Order.objects.filter(customer_phone=customer.phone)
    if request.method == 'POST':
        Interaction.objects.create(
            customer=customer,
            interaction_type=request.POST.get('type', 'call'),
            subject=request.POST.get('subject'),
            description=request.POST.get('description', ''),
        )
        messages.success(request, "Muloqot saqlandi!")
        return redirect('customer_detail', pk=pk)
    return render(request, 'crm/customer_detail.html', {
        'customer': customer, 'interactions': interactions, 'orders': orders
    })

def tasks_list(request):
    tasks = Task.objects.all()
    if request.method == 'POST':
        Task.objects.create(
            title=request.POST.get('title'),
            priority=request.POST.get('priority', 'medium'),
            due_date=request.POST.get('due_date') or None,
            description=request.POST.get('description', ''),
        )
        messages.success(request, "Vazifa qo'shildi!")
        return redirect('tasks')
    return render(request, 'crm/tasks.html', {'tasks': tasks})

def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = request.POST.get('status', task.status)
    task.save()
    return JsonResponse({'success': True})

def orders_list(request):
    orders = Order.objects.all()
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    return render(request, 'crm/orders.html', {'orders': orders, 'status_filter': status})

def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = request.POST.get('status', order.status)
    order.save()
    messages.success(request, f"Buyurtma #{pk} holati yangilandi!")
    return redirect('orders')

# ERP
def inventory(request):
    parfums = Parfum.objects.select_related('brand', 'category').all()
    movements = StockMovement.objects.all()[:15]
    low_stock = parfums.filter(stock__lt=5)
    context = {'parfums': parfums, 'movements': movements, 'low_stock': low_stock}
    return render(request, 'erp/inventory.html', context)

def add_stock(request):
    if request.method == 'POST':
        parfum = get_object_or_404(Parfum, pk=request.POST.get('parfum_id'))
        qty = int(request.POST.get('quantity', 0))
        price = float(request.POST.get('unit_price', 0))
        StockMovement.objects.create(
            parfum_name=str(parfum),
            movement_type='in',
            quantity=qty,
            unit_price=price,
        )
        parfum.stock += qty
        parfum.save()
        messages.success(request, f"{parfum.name} ga {qty} dona qo'shildi!")
    return redirect('inventory')

def finances(request):
    expenses = Expense.objects.all()[:20]
    total_expenses = Expense.objects.aggregate(s=Sum('amount'))['s'] or 0
    total_revenue = Order.objects.filter(status='delivered').aggregate(s=Sum('total_amount'))['s'] or 0
    profit = total_revenue - total_expenses
    if request.method == 'POST':
        Expense.objects.create(
            title=request.POST.get('title'),
            category=request.POST.get('category'),
            amount=request.POST.get('amount'),
            date=request.POST.get('date') or date.today(),
            description=request.POST.get('description', ''),
        )
        messages.success(request, "Xarajat qo'shildi!")
        return redirect('finances')
    return render(request, 'erp/finances.html', {
        'expenses': expenses, 'total_expenses': total_expenses,
        'total_revenue': total_revenue, 'profit': profit
    })

def suppliers(request):
    supplier_list = Supplier.objects.all()
    if request.method == 'POST':
        Supplier.objects.create(
            name=request.POST.get('name'),
            contact_person=request.POST.get('contact', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            country=request.POST.get('country', ''),
        )
        messages.success(request, "Yetkazib beruvchi qo'shildi!")
        return redirect('suppliers')
    return render(request, 'erp/suppliers.html', {'suppliers': supplier_list})

def products_manage(request):
    parfums = Parfum.objects.select_related('brand', 'category').all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_parfum':
            brand, _ = Brand.objects.get_or_create(name=request.POST.get('brand_name', 'Unknown'))
            cat, _ = Category.objects.get_or_create(
                name=request.POST.get('category_name', 'Umumiy'),
                defaults={'slug': request.POST.get('category_name', 'umumiy').lower().replace(' ', '-')}
            )
            Parfum.objects.create(
                name=request.POST.get('name'),
                brand=brand, category=cat,
                gender=request.POST.get('gender', 'female'),
                price=request.POST.get('price', 0),
                discount_price=request.POST.get('discount_price') or None,
                stock=request.POST.get('stock', 0),
                size=request.POST.get('size', '100ml'),
                description=request.POST.get('description', ''),
                top_notes=request.POST.get('top_notes', ''),
                heart_notes=request.POST.get('heart_notes', ''),
                base_notes=request.POST.get('base_notes', ''),
                is_featured=bool(request.POST.get('is_featured')),
                is_new=bool(request.POST.get('is_new', True)),
            )
            messages.success(request, "Yangi parfum qo'shildi!")
        return redirect('products_manage')
    return render(request, 'erp/products.html', {
        'parfums': parfums, 'categories': categories, 'brands': brands
    })
