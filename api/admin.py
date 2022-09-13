from django.contrib import admin
from .models import Product, Category, Order, OrderItem, Sizes

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Sizes)
