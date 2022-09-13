from cgitb import reset
from email import header
from django.shortcuts import render
from rest_framework.response import Response
from .serializer import ProductSerializer, CategorySerializer, OrderSerializer, UserSerializer
from rest_framework.generics import GenericAPIView,ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Product, Order, Category
from rest_framework import status
import json
import requests
from django.conf import settings
from .permission import UpdateOrDelete


class Signup(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProductListView(GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset=Product.objects.all()
    lookup_field = 'name'
    def get(self, request, name):
        products = Product.objects.filter(category__name=name, quantity__gt=0).order_by('-created_at')
        serializer =self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    filterset_fields = [
        'name',
        'category__name',
    ]
    search_fields = [
        'name',
        'category__name'
    ]
    
    
class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    queryset = Product.objects.order_by('-created_at')
    filterset_fields = [
        'name',
        'category__name',
    ]
    search_fields = [
        'name',
        'category__name'
    ]
    
    
class OrderView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.order_by('-created_at')
    
    def post(self, request):
        data = {}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            url = 'https://api.paystack.co/transaction/initialize'
            payload= {
                'amount':serializer.data["total_amount"]*100,
                'email':request.user.email,
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
                'order_id':serializer.data["id"]
            }
            headers = {'Authorization': f'Bearer {settings.PAYSTACK_PRIVATE_KEY}', 'Content-Type':'application/json'}
            res = requests.post(url, headers=headers, data=json.dumps(payload))
            result = res.json()
            data["data"] = serializer.data
            data["payment_redirect"] = result
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    
class OrderUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [UpdateOrDelete]
    queryset = Order.objects.order_by('-created_at')
    lookup_field = 'orderId'

    
class PayCallback(GenericAPIView):
    serializer_class=OrderSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query = request.query_params.get('trxref')
        url = f'https://api.paystack.co/transaction/verify/{query}'
        headers = {'Authorization': f'Bearer {settings.PAYSTACK_PRIVATE_KEY}'}
        res = requests.get(url, headers=headers)
        result=res.json()
        return Response({'message': result["message"]}, status=status.HTTP_200_OK)
    
class PaymentVerify(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get(self, reuest, tref):
        url = f'https://api.paystack.co/transaction/verify/{tref}'
        headers = {'Authorization': f'Bearer {settings.PAYSTACK_PRIVATE_KEY}'}
        res = requests.get(url, headers=headers)
        result=res.json()
        return Response({'message': result["message"]}, status=status.HTTP_200_OK)
        