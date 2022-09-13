from unicodedata import name
from wsgiref import validate
from rest_framework import serializers
from .models import Product, Category, Order, OrderItem, Sizes
from .utils import getUniqueId
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password'
        ]
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style':{
                    'input_type':'password'
                }
            }
        }
    def create(self, validated_data):
        user = User.objects.create(username=validated_data["email"], **validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sizes
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    size =  serializers.StringRelatedField(many=True)
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "size",
            "quantity",
            "price",
            "image",
            "category",
            "created_at",
        ]
        lookup_field = 'slug'
    
    def create(self, validated_data):
        slug = slugify(validated_data["name"])
        return Product.objects.create(slug=slug, **validated_data)
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields=[
            'price',
            'product', 
            'quantity',
            'size'
        ]


        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'orderId',
            'address',
            'phone',
            'items',
            'total_amount',
        ]
        read_only_fields =['orderId']
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        orderId = getUniqueId()
        order = Order.objects.create(orderId=orderId, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order