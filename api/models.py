from django.db import models
from django.template.defaultfilters import slugify
from io import BytesIO
from PIL import Image
from django.core.files import File
class Category(models.Model):
    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
    
    
class Product(models.Model):
    name =models.CharField(max_length=30, unique=True)
    slug = models.SlugField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    image= models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='photos/%Y/%m/%d', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(self.name)
        queryset = Product.objects.all().filter(slug__iexact=original_slug).count()
        count = 1
        slug=original_slug
        
        while(queryset):
            slug=original_slug+ '-' + str(count)
            count += 1
            queryset = Product.objects.all().filter(slug__iexact=slug).count()
        self.slug = slug
        if self.featured:
            try:
                temp = Product.objects.get(featured=True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except Product.DoesNotExist:
                pass
            
        super(Product, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name  
    
    def get_absolute_url(self):
        return f'/{self.category}/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
            
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io,name=image.name)
        return thumbnail
    
class Order(models.Model):
    orderId = models.CharField(max_length=10)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email= models.EmailField(max_length=255)
    address= models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount=models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return self.orderId
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.id}'
    
class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    paidAt = models.DateTimeField(blank=True)
    customer_code = models.CharField(max_length=30, blank=True)