from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Product
from ..serializers import ProductSerializer, UserSerializer


class ProductSerializerTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("test", "test@python.com", "aGoodPass23")

        self.product_attributes = {
            "user": user,
            "title": "Example Product",
            "notification_email": "test@product.com",
        }

        self.product = Product.objects.create(**self.product_attributes)
        self.product_serializer = ProductSerializer(instance=self.product)

    def test_serialized_output(self):
        """
        Certifies the serialized content is what's expected
        """
        expected_data = {
            "id": 1,
            "title": "Example Product",
            "notification_email": "test@product.com",
            "activation_issued": False,
            "activation_approved": None,
        }
        data = self.product_serializer.data

        self.assertEqual(data, expected_data)
