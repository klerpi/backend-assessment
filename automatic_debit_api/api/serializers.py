from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("user",)


class UserSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ("password",)
