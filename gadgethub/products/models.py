from django.db import models
from django.urls import reverse


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('smartphones', 'Smartphones'),
        ('laptops', 'Laptops'),
        ('audio', 'Audio (Headphones/Speakers)'),
        ('wearables', 'Wearables'),
        ('accessories', 'Accessories'),
        ('gaming', 'Gaming'),
        ('smart_home', 'Smart Home'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)
    brand = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)          # AI-generated or manual, final listing text
    raw_notes = models.TextField(blank=True)             # seller's rough specs/notes — feeds the AI later
    specs = models.JSONField(blank=True, null=True)      # e.g. {"RAM": "16GB", "Storage": "512GB SSD"}

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])

    @property
    def in_stock(self):
        return self.stock > 0