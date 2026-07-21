from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from products.models import Product
from .models import Cart, CartItem


def _get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_detail(request):
    cart = _get_cart(request.user)
    items = cart.items.select_related('product')
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'items': items})


@login_required
@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _get_cart(request.user)

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1
    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} of {product.name} in stock.")
        return redirect('products:detail', slug=product.slug)

    item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={'quantity': quantity}
    )
    if not created:
        item.quantity = min(item.quantity + quantity, product.stock)
        item.save()

    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('cart:detail')


@login_required
@require_POST
def cart_update(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        item.delete()
        messages.info(request, f"Removed {item.product.name} from cart.")
    else:
        item.quantity = min(quantity, item.product.stock)
        item.save()
        messages.success(request, "Cart updated.")

    return redirect('cart:detail')


@login_required
@require_POST
def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    name = item.product.name
    item.delete()
    messages.info(request, f"Removed {name} from cart.")
    return redirect('cart:detail')