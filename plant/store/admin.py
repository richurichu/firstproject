from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Banner)
admin.site.register(Color)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)

