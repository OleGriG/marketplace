from django.contrib import admin
from .models import Product, Category, ProductPhoto, Slider, Cart

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductPhoto)
admin.site.register(Slider)
admin.site.register(Cart)
# Register your models here.
