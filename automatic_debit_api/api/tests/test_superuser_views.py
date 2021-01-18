from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Product


class ApproveAndRejectProductAPITestCase(APITestCase):
    def setUp(self):
        # Setup superuser
        self.superuser = User.objects.create_user(
            "user", "test@python.com", "aGoodPass24"
        )
        self.superuser.is_superuser = True
        self.superuser.save()
        # Setup regular user
        self.user = User.objects.create_user("user2", "test@python.com", "aGoodPass244")
        # Login as superuser
        self.client.force_authenticate(user=self.superuser)
        # Create test Product
        product_attributes = {
            "user": self.user,
            "title": "Example Product",
            "notification_email": "test@product.com",
        }
        self.product = Product.objects.create(**product_attributes)

    def test_approve_product_as_superuser(self):
        get_resp = self.client.get(
            reverse("product_approve", kwargs={"pk": self.product.id})
        )
        post_resp = self.client.post(
            reverse("product_approve", kwargs={"pk": self.product.id})
        )

        self.assertEqual(get_resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(post_resp.status_code, status.HTTP_200_OK)
        self.assertTrue(post_resp.data["activation_approved"])

    def test_approve_product_as_normal_user(self):
        self.client.force_authenticate(user=self.user)

        post_resp = self.client.post(
            reverse("product_approve", kwargs={"pk": self.product.id})
        )

        expected_data = {
            "message": "You need to be the author of the product or a superuser to do this"
        }

        self.assertEqual(post_resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(post_resp.data, expected_data)

    def test_approve_product_already_approved(self):
        # Tries the same action two times
        self.client.post(reverse("product_approve", kwargs={"pk": self.product.id}))
        post_resp = self.client.post(
            reverse("product_approve", kwargs={"pk": self.product.id})
        )

        expected_data = {"message": "This product was already approved or rejected"}

        self.assertEqual(post_resp.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(post_resp.data, expected_data)

    def test_reject_product_as_superuser(self):
        get_resp = self.client.get(
            reverse("product_reject", kwargs={"pk": self.product.id})
        )
        post_resp = self.client.post(
            reverse("product_reject", kwargs={"pk": self.product.id})
        )

        self.assertEqual(get_resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(post_resp.status_code, status.HTTP_200_OK)
        self.assertFalse(post_resp.data["activation_approved"])
