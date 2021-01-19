from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("user",)
        read_only_fields = ("activation_issued", "activation_approved")


class ProductSerializerLinks(serializers.Serializer):
    id = serializers.IntegerField()
    url = serializers.HyperlinkedIdentityField(
        view_name="product_detail", lookup_field="pk"
    )


class UserSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ("password",)
