from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images')
    bannerimage = models.ImageField(upload_to='category_images')
    slug = models.SlugField(blank=True, max_length=250, unique=True)
    discount =models.PositiveIntegerField( null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('cat',kwargs={'slug': self.slug})

    


    def __str__(self):
        return self.name

class Banner(models.Model):
    name = models.CharField(max_length=50)
    image=models.ImageField(upload_to='banner_images')

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    shortdescription = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    shortdescription = models.TextField()
    slug = models.SlugField(blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'slug': self.slug})

class Color(models.Model):
    color = models.CharField(max_length=15)

    def __str__(self):
        return self.color
class ProductVariant(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    model_name=models.CharField(max_length=250)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    store_price = models.DecimalField(max_digits=10,decimal_places=2)
    sale_price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_percentage =models.PositiveIntegerField(null=True,blank=True)
    stock = models.PositiveIntegerField(default=0)
    slug = models.SlugField(blank=True,unique=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            print('------------>>>>>>>>>>><<<<<<<<<<<<---------------->>>>>>>>>>>>>><<<<<<<<<<<<<<<<')
            slug_str = f"{self.product.name} {self.color}"
            self.slug=slugify(slug_str)
        super().save(*args, **kwargs)

    def  __str__(self):
        return f"{self.product.name} - {self.color}"
    

    # def get_discounted_price(self):
    #     if self.discount_percentage is not None:
    #         discount= int(self.discount_percentage)
    #         print(f"Type of self.sale_price: {type(self.sale_price)}")
    #         print(f"Type of discount: {type(discount)}")
    #         self.sale_price = self.sale_price- (self.sale_price*discount)/100.0
    #         return self.sale_price
       
    #     return self.sale_price
    
    def get_discounted_price(self):
        category_discount= self.product.category.discount if self.product.category.discount else 0
        product_discount= self.discount_percentage if self.discount_percentage else 0 
        max_discount= max(category_discount,product_discount)
        discount = Decimal(max_discount)
        if discount > 0:
        # Calculate discounted price if there's any discount
          discounted_price = Decimal(self.sale_price) - (Decimal(self.sale_price) * discount) / 100
        else:
        # If there's no discount, then discounted_price is equal to the sale_price
          discounted_price = Decimal(self.sale_price)
        # return self.sale_price, max_discount
        discounted_price = Decimal(self.sale_price) - (Decimal(self.sale_price) * discount) / 100
        return discounted_price, max_discount
    

        # return Decimal(self.sale_price)
     
     
    # def save(self, *args, **kwargs):
    #     self.get_discounted_price()
    #     super(ProductVariant, self).save(*args, **kwargs)


    
class ProductImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.variant.product.name} - {self.variant.color}"