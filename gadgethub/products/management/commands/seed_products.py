import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from products.models import Product


def fetch_placeholder_image(seed, width=600, height=600):
    url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return ContentFile(response.content, name=f"{seed}.jpg")


PRODUCTS = [
    {"name": "iPhone 15", "slug": "iphone-15", "category": "smartphones", "brand": "Apple", "price": 999, "stock": 25,
     "specs": {"Storage": "128GB", "Color": "Black"},
     "raw_notes": "apple phone, 128gb, black colour, comes with charger cable, brand new sealed box"},

    {"name": "Samsung Galaxy S24", "slug": "galaxy-s24", "category": "smartphones", "brand": "Samsung", "price": 899, "stock": 18,
     "specs": {"Storage": "256GB", "RAM": "8GB"},
     "raw_notes": "samsung flagship, 256gb storage 8gb ram, good camera, snapdragon chip, titanium frame"},

    {"name": "Xiaomi Redmi Note 13", "slug": "redmi-note-13", "category": "smartphones", "brand": "Xiaomi", "price": 249, "stock": 40,
     "specs": {"Storage": "128GB", "RAM": "6GB"},
     "raw_notes": "budget phone but good specs, 128gb 6gb ram, big battery lasts 2 days, fast charging"},

    {"name": "MacBook Air M3", "slug": "macbook-air-m3", "category": "laptops", "brand": "Apple", "price": 1299, "stock": 12,
     "specs": {"RAM": "16GB", "Storage": "512GB SSD"},
     "raw_notes": "apple laptop, m3 chip very fast, 16gb ram 512gb ssd, silent no fan noise, great battery life all day"},

    {"name": "Dell XPS 13", "slug": "dell-xps-13", "category": "laptops", "brand": "Dell", "price": 1099, "stock": 15,
     "specs": {"RAM": "16GB", "Storage": "512GB SSD"},
     "raw_notes": "dell premium ultrabook, thin light, 16gb ram, good for students and office work, nice screen"},

    {"name": "Lenovo Legion 5", "slug": "lenovo-legion-5", "category": "laptops", "brand": "Lenovo", "price": 1399, "stock": 9,
     "specs": {"RAM": "16GB", "GPU": "RTX 4060"},
     "raw_notes": "gaming laptop, rtx 4060 graphics card, 16gb ram, runs games smoothly, rgb keyboard, heavy though"},

    {"name": "Sony WH-1000XM5", "slug": "sony-wh1000xm5", "category": "audio", "brand": "Sony", "price": 349, "stock": 30,
     "specs": {"Type": "Over-ear", "Noise Cancelling": "Yes"},
     "raw_notes": "best noise cancelling headphones, over ear comfortable for long use, 30hr battery, good for flights"},

    {"name": "AirPods Pro 2", "slug": "airpods-pro-2", "category": "audio", "brand": "Apple", "price": 249, "stock": 40,
     "specs": {"Type": "In-ear", "ANC": "Yes"},
     "raw_notes": "apple earbuds, active noise cancelling, small case, connects fast to iphone, sweat resistant"},

    {"name": "JBL Flip 6", "slug": "jbl-flip-6", "category": "audio", "brand": "JBL", "price": 129, "stock": 25,
     "specs": {"Type": "Portable Speaker", "Waterproof": "Yes"},
     "raw_notes": "bluetooth speaker, loud bass, waterproof can use near pool, 12hr battery, good for parties"},

    {"name": "Apple Watch Series 9", "slug": "apple-watch-s9", "category": "wearables", "brand": "Apple", "price": 399, "stock": 22,
     "specs": {"Size": "45mm"}, "raw_notes": "smartwatch, tracks heart rate steps sleep, works with iphone only, 45mm size fits most wrists"},

    {"name": "Samsung Galaxy Watch 6", "slug": "galaxy-watch-6", "category": "wearables", "brand": "Samsung", "price": 329, "stock": 20,
     "specs": {"Size": "44mm"}, "raw_notes": "android smartwatch, health tracking, rotating bezel, 2 day battery, matches with samsung phones"},

    {"name": "Logitech MX Master 3S", "slug": "mx-master-3s", "category": "accessories", "brand": "Logitech", "price": 99, "stock": 50,
     "specs": {"Connectivity": "Bluetooth"}, "raw_notes": "premium wireless mouse, silent clicks, works on glass surface, connects to 3 devices at once, for office use"},

    {"name": "Anker 20000mAh Power Bank", "slug": "anker-powerbank", "category": "accessories", "brand": "Anker", "price": 49, "stock": 60,
     "specs": {"Capacity": "20000mAh"}, "raw_notes": "big power bank, charges phone 4-5 times, fast charging output, good for travel"},

    {"name": "Anker USB-C Hub", "slug": "anker-usb-hub", "category": "accessories", "brand": "Anker", "price": 39, "stock": 35,
     "specs": {"Ports": "7-in-1"}, "raw_notes": "usb hub for laptop, hdmi + usb ports + sd card reader, useful for macbook users who lack ports"},

    {"name": "PlayStation 5", "slug": "ps5", "category": "gaming", "brand": "Sony", "price": 499, "stock": 8,
     "specs": {"Storage": "825GB SSD"}, "raw_notes": "gaming console, super fast loading times, comes with one controller, popular right now hard to restock"},

    {"name": "Xbox Series X", "slug": "xbox-series-x", "category": "gaming", "brand": "Microsoft", "price": 499, "stock": 10,
     "specs": {"Storage": "1TB SSD"}, "raw_notes": "xbox console, 1tb storage, 4k gaming, game pass compatible, black boxy design"},

    {"name": "DualSense Controller", "slug": "dualsense-controller", "category": "gaming", "brand": "Sony", "price": 69, "stock": 45,
     "specs": {"Compatible": "PS5"}, "raw_notes": "extra ps5 controller, haptic feedback feels realistic, comes in white, rechargeable battery"},

    {"name": "Amazon Echo Dot", "slug": "echo-dot", "category": "smart_home", "brand": "Amazon", "price": 49, "stock": 45,
     "specs": {"Gen": "5th"}, "raw_notes": "small smart speaker, alexa voice assistant, plays music sets alarms, good sound for the size"},

    {"name": "Philips Hue Starter Kit", "slug": "philips-hue-kit", "category": "smart_home", "brand": "Philips", "price": 199, "stock": 14,
     "specs": {"Bulbs": "3"}, "raw_notes": "smart light bulbs, change color from phone app, works with alexa google home, 3 bulbs plus hub included"},

    {"name": "Ring Video Doorbell", "slug": "ring-doorbell", "category": "smart_home", "brand": "Ring", "price": 99, "stock": 20,
     "specs": {"Battery": "Rechargeable"}, "raw_notes": "video doorbell, see who's at door from phone, motion alerts, easy install no wiring needed"},
]


class Command(BaseCommand):
    help = "Seed the database with realistic sample products (raw_notes filled, description left blank for AI)"

    def handle(self, *args, **options):
        count = 0
        for p in PRODUCTS:
            if Product.objects.filter(slug=p["slug"]).exists():
                continue

            product = Product(
                name=p["name"],
                slug=p["slug"],
                category=p["category"],
                brand=p["brand"],
                price=p["price"],
                stock=p["stock"],
                specs=p["specs"],
                raw_notes=p["raw_notes"],
                description="",
                is_active=True,
            )
            try:
                product.image.save(f"{p['slug']}.jpg", fetch_placeholder_image(p["slug"]), save=False)
            except requests.RequestException:
                self.stdout.write(self.style.WARNING(f"Image fetch failed for {p['slug']}, skipping image."))

            product.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {count} products (skipped existing)."))