from django.core.management.base import BaseCommand
from order.models import CartItem


class Command(BaseCommand):
    help = "Finds top 3 products for users"

    def handle(self, *args, **options):
        pass