import stripe
from django.db import models

from gamegearsite import settings
from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
class ProductCategory(models.Model):
    '''Model for category'''

    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    '''Model for our product'''

    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(decimal_places=1, max_digits=7)
    quantity = models.DecimalField(decimal_places=1, max_digits=7, default=0)
    image = models.ImageField(upload_to='product_images')
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'Product: {self.name}, Category: {self.category}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price*100), currency='usd'
        )
        return stripe_product_price

class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity
            }
            line_items.append(item)
        return line_items

class Basket(models.Model):
    '''Model for basket on the website'''

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'User: {self.user} Product: {self.product}'

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        baskets_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return baskets_item


class Review(models.Model):
    '''Review model for reviews on the website'''

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.user}, Review product: {self.product}'
