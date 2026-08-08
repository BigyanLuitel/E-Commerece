from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from products.models import Product
from .decorators import require_internal_key
import json
from django.contrib.auth import get_user_model
from django.db import transaction
from django.views.decorators.http import require_POST
from products.models import Product
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()

def _serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'category': product.category,
        'category_display': product.get_category_display(),
        'brand': product.brand,
        'description': product.description,
        'raw_notes': product.raw_notes,
        'specs': product.specs,
        'price': str(product.price),
        'stock': product.stock,
        'in_stock': product.in_stock,
        'image_url': product.image.url if product.image else None,
    }


@require_internal_key
def product_list(request):
    products = Product.objects.filter(is_active=True)
    data = [_serialize_product(p) for p in products]
    return JsonResponse({'products': data})


@require_internal_key
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    return JsonResponse(_serialize_product(product))

@csrf_exempt
@require_internal_key
@require_POST
def cart_add(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user_id = payload.get('user_id')
    product_id = payload.get('product_id')
    quantity = payload.get('quantity', 1)

    if not user_id or not product_id:
        return JsonResponse({'error': 'user_id and product_id are required'}, status=400)

    user = get_object_or_404(User, id=user_id)
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if quantity > product.stock:
        return JsonResponse({'error': f'Only {product.stock} of {product.name} in stock.'}, status=400)

    cart, _ = Cart.objects.get_or_create(user=user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
    if not created:
        item.quantity = min(item.quantity + quantity, product.stock)
        item.save()

    return JsonResponse({
        'success': True,
        'product_name': product.name,
        'quantity': item.quantity,
        'cart_total': str(cart.total_price),
    })

@csrf_exempt
@require_internal_key
@require_POST
def checkout(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user_id = payload.get('user_id')
    shipping_address = payload.get('shipping_address', '')
    payment_method = payload.get('payment_method', 'esewa')

    if not user_id:
        return JsonResponse({'error': 'user_id is required'}, status=400)

    user = get_object_or_404(User, id=user_id)

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    items = list(cart.items.select_related('product'))
    if not items:
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    for item in items:
        if item.quantity > item.product.stock:
            return JsonResponse({'error': f'Not enough stock for {item.product.name}'}, status=400)

    with transaction.atomic():
        order = Order.objects.create(user=user, shipping_address=shipping_address, payment_method=payment_method)
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

    return JsonResponse({
        'success': True,
        'order_id': order.id,
        'total': str(order.total_price),
        'payment_method': payment_method,
    })


@require_internal_key
def order_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    orders = Order.objects.filter(user=user).order_by('-created_at')[:10]

    data = [{
        'order_id': o.id,
        'status': o.status,
        'status_display': o.get_status_display(),
        'total': str(o.total_price),
        'placed_at': o.created_at.strftime('%Y-%m-%d %H:%M'),
    } for o in orders]

    return JsonResponse({'orders': data})