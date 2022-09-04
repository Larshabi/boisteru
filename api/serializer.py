from unicodedata import name
from rest_framework import serializers
from .models import Product, Category, Order, OrderItem
from .utils import getUniqueId


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = 'slug'
        
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
            'quantity'
        ]

        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'orderId',
            'first_name',
            'last_name',
            'email',
            'address',
            'place',
            'phone',
            'items',
            'total_amount'
        ]
        read_only_fields =['orderId']
    def create(self, validated_data):
        print(validated_data)
        items_data = validated_data.pop('items')
        orderId = getUniqueId()
        order = Order.objects.create(orderId=orderId, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            product = Product.objects.get(name=item_data["product"]) 
            if product.quantity == 0:
                raise serializers.ValidationError("The Product is out of stock")
            product.quantity -= item_data["quantity"]
            product.save()
        return order