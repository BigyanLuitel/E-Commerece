from django.shortcuts import render, get_object_or_404
from .models import Product

from django.db.models import Count

def home(request):
    featured = Product.objects.filter(is_active=True)[:8]
    category_counts = (
        Product.objects.filter(is_active=True)
        .values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    category_labels = dict(Product.CATEGORY_CHOICES)
    categories = [
        {'value': c['category'], 'label': category_labels.get(c['category'], c['category']), 'count': c['count']}
        for c in category_counts if c['category']
    ]
    total_products = Product.objects.filter(is_active=True).count()

    return render(request, 'products/home.html', {
        'featured': featured,
        'categories': categories,
        'total_products': total_products,
    })

def product_list(request):
    products = Product.objects.filter(is_active=True)

    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': Product.CATEGORY_CHOICES,
        'query': query or '',
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'products/product_detail.html', {'product': product})