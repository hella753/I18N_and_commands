from django.core.management.base import BaseCommand
from django.db.models import Count
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
            help="specify the max number",
        )

    def handle(self, *args, **options):
        if options["number"]:
            num = int(options["number"])
        else:
            num = 3

        products = Product.objects.annotate(popularity=Count("cart_items"))
        products = products.order_by("-popularity")

        self.stdout.write(
            self.style.SUCCESS(f"{products[:num]}")
        )