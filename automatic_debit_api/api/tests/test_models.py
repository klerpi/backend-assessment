from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("test", "test@python.com", "aGoodPass23")

        Product.objects.create(
            user=user, title="Example Product", notification_email="test@product.com"
        )

    def test_activation_approved_can_be_none(self):
        """
        Tests whether the activation_approved can be blank (None)
        This is important to validate whether the superuser processed the request or not
        """
        product = Product.objects.get(title="Example Product")
        self.assertEqual(product.activation_approved, None)

    def test_activation_issued_defaults_to_false(self):
        """
        Confirms the activation_issued defaults to False when not provided
        """
        product = Product.objects.get(title="Example Product")
        self.assertEqual(product.activation_issued, False)
