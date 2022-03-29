from django.db import models
from shop.models import Product


# Create your models here.

class Cart(models.Model):
    Cart_Id = models.CharField(max_length=250, blank=True)
    Date_Added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['Date_Added']

    def __str__(self):
        return '{}'.format(self.Cart_Id)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_tottal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return "{}".format(self.product)




