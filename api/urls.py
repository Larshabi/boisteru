from django.urls import path, include, re_path
from .views import *
urlpatterns=[
    path('products/<str:name>/', ProductListView.as_view(), name='products'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='detail'),
    path('order/', OrderView.as_view()),
    path('order/<str:orderId>/', OrderUpdateView.as_view()),
    path('paystack/callback/', PayCallback.as_view()),
    path('paystack/verify/<str:tref>/', PaymentVerify.as_view())
]