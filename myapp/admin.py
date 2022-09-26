from django.contrib import admin
from .models import Category, Product, Cart, CartProduct, Order, Admin, ProductImage

# Register your models here.
admin.site.register(Admin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(ProductImage)
