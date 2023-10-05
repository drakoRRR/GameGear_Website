from django.contrib import admin

from .models import Basket, Product, ProductCategory, Review

# Register your models here.
admin.site.register(ProductCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'stripe_product_price_id', 'category')
    list_filter = ('price', 'category')
    search_fields = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'comment', 'rate', 'created_at')
    readonly_fields = ('created_at',)

