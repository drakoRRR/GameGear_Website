from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    '''Model for category'''

    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    '''Model for our product'''

    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField()
    quantity = models.DecimalField(default=0)
    image = models.ImageField(upload_to='product_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'Product: {self.name}'

