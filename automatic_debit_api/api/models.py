from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=200)
    notification_email = models.EmailField()
    activation_issued = models.BooleanField(default=False)
    activation_approved = models.BooleanField()

    def __str__(self):
        return self.title
