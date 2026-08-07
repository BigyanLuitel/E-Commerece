from django.urls import path
from . import views

app_name = 'internal_api'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/add/', views.cart_add, name='cart_add'),
path('checkout/', views.checkout, name='checkout'),
path('orders/<int:user_id>/', views.order_status, name='order_status'),
]