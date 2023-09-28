from django.db import models

from users.models import User


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
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'Product: {self.name}, Category: {self.category}'

class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)


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
