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


class PendingProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Filters the queryset even further by showing only the
        products with activation_issued equal to true and
        products not yet approved or rejected
        """
        # Get full queryset if super user or user specific
        initial_set = get_full_queryset_if_superuser(self.request.user)
        # Get only issued products
        issued_set = initial_set.filter(activation_issued=True)
        # Get only non-approved and non-rejected products
        final_set = issued_set.filter(activation_approved__isnull=True)
        return final_set
