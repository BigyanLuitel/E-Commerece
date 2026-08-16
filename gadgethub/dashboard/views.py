from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model

from products.models import Product
from orders.models import Order
from products.forms import ProductForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from orders.models import Order
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncDate
from orders.models import Order, OrderItem

User = get_user_model()

@staff_member_required
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/product_list.html', {'products': products})


@staff_member_required
def user_list(request):
    users = User.objects.order_by('-date_joined')
    return render(request, 'dashboard/user_list.html', {
        'users': users,
        'total_users': users.count(),
    })


@staff_member_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'"{product.name}" created.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Add Product'})


@staff_member_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{product.name}" updated.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Edit Product'})


@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})
@staff_member_required
def dashboard_home(request):
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    low_stock = Product.objects.filter(stock__lt=5, is_active=True).count()

    revenue = (
        Order.objects.filter(status=Order.STATUS_PAID)
        .aggregate(total=Sum('items__price'))['total'] or 0
    )

    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]

    # --- Chart 1: Revenue over the last 14 days ---
    cutoff = timezone.now() - timedelta(days=14)
    daily_revenue = (
        Order.objects.filter(status=Order.STATUS_PAID, created_at__gte=cutoff)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Sum('items__price'))
        .order_by('day')
    )
    revenue_labels = [d['day'].strftime('%b %d') for d in daily_revenue]
    revenue_values = [float(d['total'] or 0) for d in daily_revenue]

    # --- Chart 2: Orders by status ---
    status_counts = (
        Order.objects.values('status')
        .annotate(count=Count('id'))
        .order_by('status')
    )
    status_labels = [dict(Order.STATUS_CHOICES).get(s['status'], s['status']) for s in status_counts]
    status_values = [s['count'] for s in status_counts]

    # --- Chart 3: Top 5 selling products (by quantity sold) ---
    top_products = (
        OrderItem.objects.values('product_name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:5]
    )
    top_product_labels = [p['product_name'] for p in top_products]
    top_product_values = [p['total_qty'] for p in top_products]

    # --- Chart 4: Stock levels by category ---
    stock_by_category = (
        Product.objects.filter(is_active=True)
        .values('category')
        .annotate(total_stock=Sum('stock'))
        .order_by('category')
    )
    category_labels_map = dict(Product.CATEGORY_CHOICES)
    stock_labels = [category_labels_map.get(c['category'], c['category'] or 'Uncategorized') for c in stock_by_category]
    stock_values = [c['total_stock'] or 0 for c in stock_by_category]

    return render(request, 'dashboard/home.html', {
        'total_products': total_products,
        'active_products': active_products,
        'low_stock': low_stock,
        'revenue': revenue,
        'recent_orders': recent_orders,
        'revenue_labels': json.dumps(revenue_labels),
        'revenue_values': json.dumps(revenue_values),
        'status_labels': json.dumps(status_labels),
        'status_values': json.dumps(status_values),
        'top_product_labels': json.dumps(top_product_labels),
        'top_product_values': json.dumps(top_product_values),
        'stock_labels': json.dumps(stock_labels),
        'stock_values': json.dumps(stock_values),
    })
    
@staff_member_required
def order_list(request):
    orders = Order.objects.select_related('user').order_by('-created_at')

    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)

    return render(request, 'dashboard/order_list.html', {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'selected_status': status or '',
    })


@staff_member_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} marked as {order.get_status_display()}.")
            return redirect('dashboard:order_detail', pk=order.pk)

    return render(request, 'dashboard/order_detail.html', {'order': order})


@staff_member_required
@require_POST
def generate_description(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    ai_payload = {
        "name": payload.get("name", ""),
        "category": payload.get("category", ""),
        "brand": payload.get("brand", ""),
        "raw_notes": payload.get("raw_notes", ""),
        "specs": payload.get("specs") or None,
    }
    try:
        response = requests.post(
            "http://localhost:8010/products/generate-description",
            json=ai_payload,
            timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({"error": f"AI service unavailable: {str(e)}"}, status=502)

    return JsonResponse(response.json())

@staff_member_required
@require_POST
def suggest_category(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request data."}, status=400)

    ai_payload = {
        "name": payload.get("name", ""),
        "raw_notes": payload.get("raw_notes", ""),
    }

    try:
        response = requests.post(
            "http://localhost:8010/products/suggest-category",
            json=ai_payload,
            timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({"error": f"AI service unavailable: {str(e)}"}, status=502)

    return JsonResponse(response.json())