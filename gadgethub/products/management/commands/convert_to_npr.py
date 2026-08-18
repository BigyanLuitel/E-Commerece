from decimal import Decimal
from django.core.management.base import BaseCommand
from products.models import Product

# Rough USD → NPR conversion, rounded to feel like realistic retail pricing
CONVERSION_RATE = Decimal("140")


class Command(BaseCommand):
    help = "Converts existing product prices from USD-style numbers to NPR-style numbers (run once)"

    def handle(self, *args, **options):
        updated = 0
        for product in Product.objects.all():
            new_price = (product.price * CONVERSION_RATE).quantize(Decimal("1"))
            # round to nearest 10 so it doesn't look like a raw conversion
            new_price = (new_price / 10).quantize(Decimal("1")) * 10
            product.price = new_price
            product.save(update_fields=["price"])
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Converted {updated} product prices to NPR."))