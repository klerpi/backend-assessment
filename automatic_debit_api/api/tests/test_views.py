from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class ProductListAPITestCase(APITestCase):
    def setUp(self):
        # Set up regular user
        self.user = User.objects.create_user("user", "test@python.com", "aGoodPass24")
        self.client.force_authenticate(user=self.user)  # Default logged in user

        self.empty_response = {
            "count": 0,  # No products yet
            "next": None,
            "previous": None,
            "results": [],
        }

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)  # Logs out
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_access(self):
        response = self.client.get(reverse("product_list"))
        data = dict(response.data)  # From OrderedDict to dict

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, self.empty_response)

    def test_new_product(self):
        new_product = {
            "title": "Test Product",
            "notification_email": "test@example.com",
        }
        response = self.client.post(reverse("product_list"), new_product)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["activation_issued"], False)
        self.assertIsNone(response.data["activation_approved"])

    def test_other_user_cant_see_new_product(self):
        user2 = User.objects.create_user("user2", "test@python.com", "aGoodPass25")
        self.client.force_authenticate(user=user2)

        response = self.client.get(reverse("product_list"))
        data = dict(response.data)  # From OrderedDict to dict

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, self.empty_response)
