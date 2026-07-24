from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from cart.models import Cart
from .models import Order, OrderItem

@login_required
@require_POST
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('products:list')

    items = list(cart.items.select_related('product'))
    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect('products:list')

    for item in items:
        if item.quantity > item.product.stock:
            messages.error(request, f"Not enough stock for {item.product.name}.")
            return redirect('cart:detail')

    shipping_address = request.POST.get('shipping_address', '')
    payment_method = request.POST.get('payment_method', 'esewa')

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            payment_method=payment_method,
        )
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )
            item.product.stock -= item.quantity
            item.product.save()
        cart.items.all().delete()

    return redirect('orders:payment', order_id=order.id)

import random
import string


def _generate_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == Order.STATUS_PAID:
        return redirect('orders:detail', order_id=order.id)

    return render(request, 'orders/payment.html', {'order': order})


@login_required
@require_POST
def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != Order.STATUS_PAID:
        order.status = Order.STATUS_PAID
        order.transaction_id = _generate_transaction_id()
        order.paid_at = timezone.now()
        order.save()

    messages.success(request, f"Payment successful. Order #{order.id} confirmed.")
    return redirect('orders:detail', order_id=order.id)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})