from django.db import models
from django.utils.translation import gettext_lazy as _


class Checkout(models.Model):
    order_notes = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("შეკვეთის დეტალები")
    )
    order_date = models.DateField(
        auto_now_add=True,
        verbose_name=_("შეკვეთის თარიღი")
    )
    product_cart = models.ForeignKey(
        "order.Cart",
        on_delete=models.CASCADE,
        verbose_name=_("მომხმარებლის კალათა"),
    )

    def __str__(self):
        return f"Order {self.id}"

