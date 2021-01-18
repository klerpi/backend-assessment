from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Product


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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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


class ProductDetailAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@python.com", "aGoodPass24")

        self.product_attributes = {
            "user": self.user,
            "title": "Example Product",
            "notification_email": "test@product.com",
        }
        self.product = Product.objects.create(**self.product_attributes)

        self.client.force_authenticate(user=self.user)  # Default logged in user

        self.expected_data = {
            "id": self.product.id,
            "title": "Example Product",
            "notification_email": "test@product.com",
            "activation_issued": False,
            "activation_approved": None,
        }

    def test_product_details_retrieved(self):
        response = self.client.get(
            reverse("product_detail", kwargs={"pk": self.product.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data)

    def test_product_update(self):
        self.expected_data["title"] = "The title changed!"

        response = self.client.put(
            reverse("product_detail", kwargs={"pk": self.product.id}),
            self.expected_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.expected_data["title"])

    def test_product_delete(self):
        delete_resp = self.client.delete(
            reverse("product_detail", kwargs={"pk": self.product.id})
        )
        get_resp = self.client.get(
            reverse("product_detail", kwargs={"pk": self.product.id})
        )

        self.assertEqual(delete_resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_resp.status_code, status.HTTP_404_NOT_FOUND)


class ProductActivationAndCancelationAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user("test", "test@python.com", "aGoodPass24")
        self.client.force_authenticate(user=user)  # Default logged in user

        product_attributes = {
            "user": user,
            "title": "Example Product",
            "notification_email": "test@product.com",
        }
        self.product = Product.objects.create(**product_attributes)

    def test_activation_of_a_product(self):
        get_resp = self.client.get(
            reverse("product_activate", kwargs={"pk": self.product.id})
        )
        post_resp = self.client.post(
            reverse("product_activate", kwargs={"pk": self.product.id})
        )

        self.assertEqual(get_resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(post_resp.status_code, status.HTTP_200_OK)
        self.assertTrue(post_resp.data["activation_issued"])

    def test_cancelation_of_a_product(self):
        get_resp = self.client.get(
            reverse("product_cancel", kwargs={"pk": self.product.id})
        )
        post_resp = self.client.post(
            reverse("product_cancel", kwargs={"pk": self.product.id})
        )

        self.assertEqual(get_resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(post_resp.status_code, status.HTTP_200_OK)
        self.assertFalse(post_resp.data["activation_issued"])


class PendingProductsAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user("test", "test@python.com", "aGoodPass24")
        self.client.force_authenticate(user=user)  # Default logged in user

        product_attributes = {
            "user": user,
            "title": "Example Product",
            "notification_email": "test@product.com",
        }
        self.product = Product.objects.create(**product_attributes)

    def test_product_appearing_after_activation(self):
        # Activate the product
        self.client.post(reverse("product_activate", kwargs={"pk": self.product.id}))
        # Get pending list
        response = self.client.get(reverse("product_pending_list"))

        expected_data = [
            {
                "id": self.product.id,
                "title": "Example Product",
                "notification_email": "test@product.com",
                "activation_issued": True,
                "activation_approved": None,
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], expected_data)

    def test_product_not_appearing_after_cancelation(self):
        # Cancel the product
        self.client.post(reverse("product_cancel", kwargs={"pk": self.product.id}))
        # Get pending list
        response = self.client.get(reverse("product_pending_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])
