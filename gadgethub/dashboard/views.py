from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum, Count

from products.models import Product
from orders.models import Order
from products.forms import ProductForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from orders.models import Order

@staff_member_required
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/product_list.html', {'products': products})


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

    total_orders = Order.objects.count()
    revenue = (
        Order.objects.filter(status=Order.STATUS_PAID)
        .aggregate(total=Sum('items__price'))['total'] or 0
    )

    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]

    return render(request, 'dashboard/home.html', {
        'total_products': total_products,
        'active_products': active_products,
        'low_stock': low_stock,
        'total_orders': total_orders,
        'revenue': revenue,
        'recent_orders': recent_orders,
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