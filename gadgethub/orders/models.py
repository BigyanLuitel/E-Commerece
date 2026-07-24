from django.conf import settings
from django.db import models
from products.models import Product


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    PAYMENT_ESEWA = 'esewa'
    PAYMENT_KHALTI = 'khalti'
    PAYMENT_CARD = 'card'
    PAYMENT_CHOICES = [
        (PAYMENT_ESEWA, 'eSewa'),
        (PAYMENT_KHALTI, 'Khalti'),
        (PAYMENT_CARD, 'Credit/Debit Card'),
    ]


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    shipping_address = models.TextField(blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, blank=True)
    transaction_id = models.CharField(max_length=50, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} ({self.user.email})"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    @property
    def subtotal(self):
        return self.price * self.quantity