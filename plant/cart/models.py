from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from store.models import *
from .models import *
from decimal import Decimal
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.pk} for {self.user.username}"

    def get_total_price(self):
        return self.cartitems_set.aggregate(total_price=Sum('price'))['total_price']

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField( max_digits=8, decimal_places=2)



    def get_item_price(self):
        return Decimal(self.price) * Decimal(self.quantity)