from rest_framework import generics, views

from ..models import Product

from .view_helpers import toggle_activation_approved


class ApproveProductAPIView(views.APIView):
    def post(self, request, pk=None):
        product = generics.get_object_or_404(Product, pk=pk)
        return toggle_activation_approved(request.user, product, new_value=True)


class RejectProductAPIView(views.APIView):
    def post(self, request, pk=None):
        product = generics.get_object_or_404(Product, pk=pk)
        return toggle_activation_approved(request.user, product, new_value=False)
