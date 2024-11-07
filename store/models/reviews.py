from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ProductReviews(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("ავტორი")
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        verbose_name=_("პროდუქტი")
    )
    date = models.DateField(auto_now_add=True, verbose_name=_("თარიღი"))
    review = models.TextField(verbose_name=_("რევიუ"))


class ShopReviews(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("ავტორი")
    )
    review = models.TextField(verbose_name=_("რევიუ"))
    date = models.DateField(auto_now_add=True, verbose_name=_("თარიღი"))

    def __str__(self):
        return f"{self.id}"


