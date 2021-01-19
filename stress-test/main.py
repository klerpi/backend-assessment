import os
from locust import HttpUser, task


class WebsiteUser(HttpUser):
    def on_start(self):
        credentials = {
            "username": os.environ.get("DJANGO_SUPERUSER_USERNAME"),
            "password": os.environ.get("DJANGO_SUPERUSER_PASSWORD"),
        }

        with self.client.post("/token/", json=credentials) as response:
            token = response.json()["access"]
            self.auth_header = {"Authorization": "Bearer " + token}

    @task
    def get_products(self):
        self.client.get(url="/products/", headers=self.auth_header)
