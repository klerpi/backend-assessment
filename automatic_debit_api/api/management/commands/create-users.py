import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Creates the superuser provided in the .env file if it doesn't exists already
    Also creates a regular user
    Useful for fresh installs of the project
    """

    help = "Creates the superuser and normal user provided in the .env if it doesn't exists already"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")

        if not User.objects.filter(username=username).exists():
            call_command("createsuperuser", interactive=False)
        else:
            print("Superuser already created. Continuing...")

        if not User.objects.filter(username="user").exists():
            username = os.environ.get("REGULAR_USER_USERNAME")
            password = os.environ.get("REGULAR_USER_PASSWORD")
            User.objects.create_user(username=username, password=password)
        else:
            print("Regular user already created. Continuing...")
