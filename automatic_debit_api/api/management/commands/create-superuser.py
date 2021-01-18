import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Creates the superuser provided in the .env file if it doesn't exists already
    Useful for fresh installs of the project
    """

    help = "Creates the superuser provided in the env vars if it doesn't exists already"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")

        if User.objects.filter(username=username).exists():
            print("Superuser already created. Continuing...")
        else:
            call_command("createsuperuser", interactive=False)
