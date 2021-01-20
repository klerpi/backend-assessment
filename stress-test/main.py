import os
import string
import random
from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_header = ""
        self.credentials = {
            "username": os.environ.get("DJANGO_SUPERUSER_USERNAME"),
            "password": os.environ.get("DJANGO_SUPERUSER_PASSWORD"),
        }
        self.refresh_token = ""

    wait_time = between(1, 5)

    def login(self):
        """
        Gets a token for authorized requests and defines the Authorization header
        """
        with self.client.post("/token/", json=self.credentials) as response:
            token = response.json()["access"]
            self.refresh_token = response.json()["refresh"]
            self.auth_header = {"Authorization": "Bearer " + token}

    def refresh_login(self):
        """
        Refreshes expired tokens
        """
        body = {"refresh": self.refresh_token}

        with self.client.post("/token/", json=body) as response:
            token = response.json()["access"]
            self.auth_header = {"Authorization": "Bearer " + token}

    def on_start(self):
        """
        Initialization before starting the tests
        """
        self.login()

    def get_random_string(self):
        """
        Generates a string with 10 random letters
        """
        letters = string.ascii_letters
        return "".join(random.choice(letters) for _ in range(10))

    def get_random_email(self):
        """
        Generates a randomized email
        """
        user = self.get_random_string()
        domain = self.get_random_string()
        return f"{user}@{domain}.com"

    @task
    def get_products(self):
        self.client.get(url="/products/", headers=self.auth_header)

    @task
    def new_product(self):
        data = {
            "title": self.get_random_string(),
            "notification_email": self.get_random_email(),
        }

        self.client.post(
            url="/products/",
            json=data,
            headers=self.auth_header,
        )
