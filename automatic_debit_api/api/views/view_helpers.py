from rest_framework import status
from rest_framework.response import Response

from ..models import Product
from ..serializers import ProductSerializer


def get_full_queryset_if_superuser(user):
    """
    Returns the full queryset if the current user is a superuser
    Otherwise, it returns only products created by the current user
    """
    if user.is_superuser:
        return Product.objects.all()
    else:
        return Product.objects.filter(user=user)


def toggle_activation_issued(user, product, new_value):
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
