from rest_framework import serializers
from .models import Product,Profile
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source="product.all")
    
    class Meta:
        model = Profile
        fields = ['product','serial']

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = '__all__'

