from django.core.management.base import BaseCommand
from order.models import CartItem
from store.models import Product


class Command(BaseCommand):
    help = "Finds top 3 products for users"

    def handle(self, *args, **options):
        list_of_amounts = []
        dct = {}
        for product in Product.objects.iterator():
            amount = CartItem.objects.filter(product=product).count()
            dct.update({product:amount})
            list_of_amounts.append(amount)
        sorted_list = sorted(list_of_amounts, reverse=True)[:3]
        result = []
        for num in sorted_list:
            for key, value in dct.items():
                if num==value:
                    result.append((key, value))

        self.stdout.write(
            self.style.SUCCESS(f"{result}")
        )