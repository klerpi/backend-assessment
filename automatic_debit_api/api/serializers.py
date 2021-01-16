from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Product


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("user",)
