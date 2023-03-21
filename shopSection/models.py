from django.db import models
import string,random
from django.contrib.auth.models import User

def id_gen(size=7, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=30 ,blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.PositiveIntegerField(default=0)
    discount_price = models.PositiveIntegerField(default=0, editable=False)
    price = models.PositiveIntegerField()
    stock_status = models.BooleanField(default=True, blank=True, editable=False)
    product_pic = models.ImageField(upload_to='products/', default='product.jpg')
    description = models.TextField(null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)
    def save(self):
        if self.quantity == 0:
            self.stock_status = False
        if self.discount != 0:
            discount_percent = self.price * (self.discount / 100)
            self.discount_price = self.price - discount_percent
        if self.product_id == None:
            self.product_id = self.name[:6] + '_' + id_gen()

        return super(Product, self).save()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    cartPrice = models.FloatField(default=0.00, null=True)

    def __str__(self):
        return str(self.user)
    
    def save(self, *args, **kwargs):
        if self.cartPrice == 0.00:
            if self.product.discount > 0:
                self.cartPrice = self.product.discount_price * self.quantity
            else:
                self.cartPrice = self.product.price * self.quantity
        return super(Cart, self).save()

