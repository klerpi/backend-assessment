from rest_framework import generics, views
from django.contrib.auth.models import User

from ..models import Product
from ..serializers import ProductSerializer

from .view_helpers import (
    get_full_queryset_if_superuser,
    toggle_activation_issued,
)


class ProductListAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return get_full_queryset_if_superuser(self.request.user)

    def perform_create(self, serializer):
        """
        Binds the new product to the current user
        """
        user_pk = self.request.user.id
        user = generics.get_object_or_404(User, pk=user_pk)
        serializer.save(user=user)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return get_full_queryset_if_superuser(self.request.user)


class ProductActivationRequestAPIView(views.APIView):
    def post(self, request, pk=None):
        product = generics.get_object_or_404(Product, pk=pk)
        return toggle_activation_issued(request.user, product, new_value=True)


class ProductActivationCancelationAPIView(views.APIView):
    def post(self, request, pk=None):
        product = generics.get_object_or_404(Product, pk=pk)
        return toggle_activation_issued(request.user, product, new_value=False)
