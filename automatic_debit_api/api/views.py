from rest_framework import generics
from django.contrib.auth.models import User

from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_superuser:
            return Product.objects.all()
        else:
            return Product.objects.filter(user=current_user)

    def perform_create(self, serializer):
        user_pk = self.request.user.id
        user = generics.get_object_or_404(User, pk=user_pk)
        serializer.save(user=user)
