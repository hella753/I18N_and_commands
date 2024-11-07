from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db.models import Count
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, FormView
from mixins.search_mixin import SearchMixin
from store.forms import ContactForm
from store.models import Product, ProductReviews
from store.models import Category, ShopReviews, ProductTags


class IndexView(SearchMixin, ListView):
    model = ShopReviews
    template_name = "homepage/index.html"
    queryset = ShopReviews.objects.select_related("user")
    context_object_name = "reviews"


class CategoryListingsView(ListView):
    """
    filters:
    'q' -> search
    't' -> tags
    'p' -> price
    'fruitlist' -> sorting
    """
    model = Product
    template_name = "shop/shop.html"
    paginate_by = 6

    def get_queryset(self):
        category_slug = self.kwargs.get("slug")
        if category_slug:
            cache_key = f"products_{category_slug}"
            queryset = cache.get(cache_key)
            if queryset is None:
                category = Category.objects.filter(slug=category_slug)
                categories = category.get_descendants(include_self=True)
                queryset = (
                    super().get_queryset()
                    .filter(product_category__in=categories)
                    .prefetch_related("tags")
                )
                cache.set(cache_key, queryset, 60)
        else:
            cache_key = "products"
            queryset = cache.get(cache_key)
            if queryset is None:
                queryset = super().get_queryset().prefetch_related(
                    "product_category",
                    "tags"
                )
                cache.set(cache_key, queryset, 60)

        search = self.request.GET.get('q')
        tag = self.request.GET.get('t')
        price = self.request.GET.get('p')
        fruit_list = self.request.GET.get("fruitlist")
        if search or tag or price or fruit_list:
            cache_filter_key = f"filtered_queryset_{queryset}"
            queryset = cache.get(cache_filter_key)
            if queryset is None:
                queryset = cache.get("products").filter(
                    product_name__icontains=search
                )
                if price:
                    queryset = queryset.filter(
                        product_price__lte=float(price)
                    )
                if fruit_list == "2":
                    queryset = queryset.order_by("product_price")
                if tag:
                    tags = tag
                    queryset = queryset.filter(tags__in=tags)
                queryset = queryset.prefetch_related("tags")
                cache_filter_key = f"filtered_queryset_{queryset}"
                cache.set(cache_filter_key, queryset, 60)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_tags = cache.get("product_tags")
        if product_tags is None:
            product_tags = ProductTags.objects.all()
            cache.set("product_tags", product_tags, 60)

        category_slug = self.kwargs.get("slug")
        if category_slug:
            cache_key = f"categories_{category_slug}"
            category_cache_key = category_slug
            if cache.get(category_cache_key) is None:
                category = Category.objects.filter(slug=category_slug)
                cache.set(category_cache_key, category, 60)
            if cache.get(cache_key) is None:
                categories = (
                    cache.get(category_cache_key)
                    .get_descendants(include_self=False)
                    .annotate(
                        count=Count("product") + Count('children__product')
                    )
                )
                cache.set(cache_key, categories, 60)
            context["categories"] = cache.get(cache_key)
        else:
            cache_key = "categories"
            if cache.get(cache_key) is None:
                categories = (
                    Category.objects.all()
                    .get_descendants(include_self=True)
                    .annotate(
                        count=Count('product') + Count('children__product')
                    )
                    .filter(parent__isnull=True)
                )
                cache.set(cache_key, categories, 60)
            context["categories"] = cache.get(cache_key)
        context["product_tags"] = cache.get("product_tags")
        return context


class ContactView(SearchMixin, FormView):
    template_name = "contact/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("store:contact")

    def form_valid(self, form):
        sender_name = form.cleaned_data["sender_name"]
        sender_email = form.cleaned_data["sender_email"]
        message = form.cleaned_data["message"]
        mail = EmailMessage(
            f"New Message from {sender_name}",
            body=message,
            from_email=sender_email,
            to=["kristigaphrindashvili@gmail.com"],
        )
        # from_email is not working properly so adding
        # reply_to to be able to reply to the sender.
        mail.reply_to = [sender_email]
        mail.send(fail_silently=False)
        messages.success(self.request, _('შეტყობინება წარმატებით გაიგზავნა!'))
        return super().form_valid(form)


class ProductView(SearchMixin, DetailView):
    model = Product
    template_name = "product_detail/shop-detail.html"
    pk_url_kwarg = "id"
    queryset = Product.objects.prefetch_related("product_category", "tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_reviews = ProductReviews.objects.filter(
            product=self.object
        ).select_related("user")
        quantity = 1

        context["reviews"] = product_reviews
        context["quantity"] = quantity
        return context


class PageNotFound(TemplateView):
    template_name = '404.html'


# For testing set DEBUG to False and visit "test500/"
class InternalServerError(View):
    def get(self, request, *args, **kwargs):
        raise Exception
