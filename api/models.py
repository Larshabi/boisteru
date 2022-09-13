from django.db import models
from django.template.defaultfilters import slugify
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib.auth.models import User

class Category(models.Model):
    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
    
    
class Product(models.Model):
    name =models.CharField(max_length=30, unique=True)
    description=models.CharField(max_length=255, blank=True)
    slug = models.SlugField(null=True, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    image= models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=0)
    
    
        
    def __str__(self):
        return self.name  
    
    def get_absolute_url(self):
        return f'/{self.category}/{self.slug}/'
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    orderId = models.CharField(max_length=10)
    address= models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount=models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.orderId
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=20, blank=True, null=True)
    
    
    def __str__(self):
        return f'{self.id}'
    
class Sizes(models.Model):
    class Meta:
        verbose_name_plural='Sizes'
    product = models.ForeignKey(Product, related_name='size', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.name}'
    
class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    paidAt = models.DateTimeField(blank=True)
    customer_code = models.CharField(max_length=30, blank=True)