from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'stock', 'is_active']
    list_filter = ['category', 'brand', 'is_active']
    search_fields = ['name', 'brand', 'description']
    prepopulated_fields = {'slug': ('name',)}