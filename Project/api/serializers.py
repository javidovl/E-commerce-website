from django.db.models import fields
from rest_framework import serializers
from product.models import Category, Product, Review_Product
from checkout.models import *
from django.contrib.auth import get_user_model
from core.models import *
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id","name","price","description","category","category_name", "sizes_in_stock", "colors_of_product"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Category


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Basket
        fields=['id', 'user', 'product_list' ,'product_features', 'total_price']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=['name', 'email', 'phone_number', 'password']

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review_Product
        fields=['reviewer_name', 'reviewer_email', 'review_text', 'review_star', 'product_id']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wishlist
        fields=['user', 'product_list']

class ProductVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductVersion
        fields=['id','product', 'size', 'color', 'price', 'in_stock', 'stock_quantity', 'name', 'price', 'description','category','category_name', 'sizes_in_stock', 'colors_of_product', 'image_url', 'review_count']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['user', 'basket', 'billing_address']