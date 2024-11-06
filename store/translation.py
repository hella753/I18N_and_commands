from modeltranslation.translator import TranslationOptions, register, translator
from .models import Product, Category, ProductTags


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(ProductTags)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('tag_name',)
