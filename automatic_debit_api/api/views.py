from rest_framework import generics, status, views
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Product
from .serializers import ProductSerializer


# Helper functions
def get_full_queryset_if_superuser(user):
    """
    Returns the full queryset if the current user is a superuser
    Otherwise, it returns only products created by the current user
    """
    if user.is_superuser:
        return Product.objects.all()
    else:
        return Product.objects.filter(user=user)


def toggle_activation_issued_if_author_or_superuser(user, product, new_value):
    """
    Sets the activation_issued property to new_value and returns the Response object
    Property is only set if the current user is the author of the product or a superuser
    Otherwise an error message is sent instead
    """
    if user == product.user or user.is_superuser:
        product.activation_issued = new_value
        product.save()
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data)
    else:
        return Response(
            {
                "message": "You need to be the author of the product or a superuser to do this"
            },
            status=status.HTTP_403_FORBIDDEN,
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
        return toggle_activation_issued_if_author_or_superuser(
            request.user, product, new_value=True
        )
