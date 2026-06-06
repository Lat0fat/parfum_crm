from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Sum, Q

from crm.models import Customer, Interaction, Task
from erp.models import Order, Parfum, Expense


def dashboard(request):
    now = timezone.now()
    orders_qs = Order.objects.all()
    month_qs = orders_qs.filter(created_at__year=now.year, created_at__month=now.month)

    total_revenue = orders_qs.aggregate(s=Sum('total_amount'))['s'] or 0
    month_revenue = month_qs.aggregate(s=Sum('total_amount'))['s'] or 0

    context = {
        'total_orders': orders_qs.count(),
        'month_orders': month_qs.count(),
        'total_revenue': total_revenue,
        'month_revenue': month_revenue,
        'total_customers': Customer.objects.count(),
        'new_customers': Customer.objects.filter(created_at__year=now.year, created_at__month=now.month).count(),
        'pending_orders': orders_qs.filter(status='new').count(),
        'low_stock': Parfum.objects.filter(stock__lt=5).count(),
        'tasks_due': Task.objects.exclude(status='done').count(),
        'recent_orders': orders_qs.order_by('-created_at')[:10],
        'top_parfums': Parfum.objects.order_by('-sold_count')[:5],
    }
    return render(request, 'crm/dashboard.html', context)


def customers_list(request):
    qs = Customer.objects.all()
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(phone__icontains=q))
    if status:
        qs = qs.filter(status=status)
    return render(request, 'crm/customers.html', {'customers': qs, 'status': status})


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        Interaction.objects.create(
            customer=customer,
            interaction_type=request.POST.get('type', 'call'),
            subject=request.POST.get('subject', ''),
            description=request.POST.get('description', ''),
        )
        return redirect('customer_detail', pk=pk)
    context = {
        'customer': customer,
        'orders': customer.orders.all(),
        'interactions': customer.interactions.all(),
    }
    return render(request, 'crm/customer_detail.html', context)


def tasks_list(request):
    if request.method == 'POST':
        Task.objects.create(
            title=request.POST.get('title', ''),
            priority=request.POST.get('priority', 'medium'),
            due_date=request.POST.get('due_date') or None,
            description=request.POST.get('description', ''),
        )
        return redirect('tasks')
    return render(request, 'crm/tasks.html', {'tasks': Task.objects.all()})


def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.status = request.POST.get('status', task.status)
        task.save()
    return redirect('tasks')


def orders_list(request):
    qs = Order.objects.all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'crm/orders.html', {'orders': qs, 'status_filter': status_filter})


def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = request.POST.get('status', order.status)
        order.save()
    return redirect('orders')
