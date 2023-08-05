from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from store.models import *
from .models import *
from decimal import Decimal
# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    minimum_order_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    single_use_per_user = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)


class Cart(models.Model):
    user = models.ForeignKey(User, blank= True, null= True, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL) 
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True,blank=True)

    # def __str__(self):
    #     return f"Cart {self.pk} for {self.user.username}"


    
    def get_total_price(self):
        return self.cartitems_set.aggregate(total_price=Sum('price'))['total_price']
    
    

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField( max_digits=8, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)


    @property
    def item_price(self):
        return Decimal(self.product.sale_price) * Decimal(self.quantity)
    
    # @property
    # def discounted_item_price(self):
    #     discounted_price, _ = self.product.get_discounted_price()
    #     return Decimal(discounted_price) * self.quantity
    
    @property
    def discounted_item_price(self):
        result = self.product.get_discounted_price()
        print("Result of get_discounted_price: ", result)
        discounted_price, _ = self.product.get_discounted_price()
        return  Decimal(discounted_price) * int(self.quantity)

    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Wishlist for {self.user.username}"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

    def get_item_price(self):
        return self.product.sale_price
    
