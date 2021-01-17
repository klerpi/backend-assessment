from rest_framework import generics
from django.contrib.auth.models import User

from .models import Product
from .serializers import ProductSerializer


# Helper function
def get_full_queryset_if_superuser(user):
    """
    Returns the full queryset if the current user is a superuser
    Otherwise, it returns only products created by the current user
    """
    if user.is_superuser:
        return Product.objects.all()
    else:
        return Product.objects.filter(user=user)


class ProductListAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        current_user = self.request.user
        return get_full_queryset_if_superuser(current_user)

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
