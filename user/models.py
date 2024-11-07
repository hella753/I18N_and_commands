from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, password, **other_fields):
        if not username:
            raise ValueError("Required Field Email is not set")
        if not password:
            raise ValueError("Required Field Password is not set")
        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **other_fields):
        if not username:
            raise ValueError("Required Field Email is not set")
        if not password:
            raise ValueError("Required Field Password is not set")
        user = self.create_user(username, password, **other_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("ელ. ფოსტა")
    )
    username = models.CharField(
        max_length=20,
        unique=True,
        help_text="Required. 20 characters or fewer",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists."
        },
        verbose_name=_("მომხმარებლის სახელი")
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("შექმნის თარიღი")
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("სახელი")
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("გვარი")
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
        verbose_name=_("სტაფის სტატუსი")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("აქტიურობის სტატუსი")
    )

    order_address = models.CharField(
        max_length=100,
        verbose_name=_("მისამართი"),
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("ქალაქი")
    )
    country = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("ქვეყანა")
    )
    postcode = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("საფოსტო კოდი")
    )
    mobile = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("ტელეფონის ნომერი")
    )

    last_active_datetime = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("ბოლო აქტიურობის თარიღი")
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}"
