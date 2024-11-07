from django.core.management.base import BaseCommand
from order.models import CartItem
from store.models import Product


class Command(BaseCommand):
    """
    This command prints the top X products by popularity.
    You can specify X by using the --number argument.
    Default is 3.
    """
    help = "Finds the most popular products for users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            action="store",
            help="specify the max number",
        )

    def handle(self, *args, **options):
        list_of_amounts = []
        dct = {}

        if options["number"]:
            num = int(options["number"])
        else:
            num = 3

        for product in Product.objects.iterator():
            amount = CartItem.objects.filter(product=product).count()
            dct.update({product: amount})
            list_of_amounts.append(amount)
        sorted_list = sorted(list_of_amounts, reverse=True)[:num]
        result = []

        for num in sorted_list:
            for key, value in dct.items():
                if num == value and (key, value) not in result:
                    result.append((key, value))

        self.stdout.write(
            self.style.SUCCESS(f"{result}")
        )
