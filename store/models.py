from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from versatileimagefield.fields import VersatileImageField
from django.utils.translation import gettext_lazy as _


class Category(MPTTModel):
    category_name = models.CharField(max_length=100, null=True, verbose_name=_("სახელი"))
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("ზეკატეგორია"),
        related_name="children"
    )
    slug = models.SlugField(default="", blank=True, verbose_name=_("სლაგი"))

    class MPTTMeta:
        order_insertion_by = ['category_name']

    def __str__(self):
        return f"{self.category_name}"


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name=_("სახელი"))
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("ფასი")
    )
    product_description = models.TextField(null=True, blank=True, verbose_name=_("აღწერა"))
    product_rating = models.IntegerField(null=True, blank=True, verbose_name=_("შეფასება"))
    product_image = VersatileImageField(
        help_text=_("ატვირთეთ ფოტოსურათი"),
        blank=True,
        null=True,
        verbose_name=_("სურათი")
    )
    product_category = models.ManyToManyField(
        "Category",
        verbose_name=_("კატეგორია")
    )
    product_quantity = models.IntegerField(null=True, blank=True, verbose_name=_("მარაგშია:"))
    country = models.CharField(default="Agro Farm", max_length=150, verbose_name=_("ქვეყანა"))
    weight = models.PositiveIntegerField(default=1, verbose_name=_("წონა"))
    slug = models.SlugField(default="", unique=True, blank=True, verbose_name=_("სლაგი"))
    tags = models.ManyToManyField("ProductTags", blank=True, verbose_name=_("ტეგები"))

    def __str__(self):
        return f"{self.product_name}"


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


class ProductTags(models.Model):
    tag_name = models.CharField(max_length=150, verbose_name=_("სახელი"))
