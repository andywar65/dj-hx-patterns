from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create superuser."

    def handle(self, *args, **options):
        if settings.DEBUG is False:
            raise CommandError("This command cannot be run when DEBUG is False.")

        self.stdout.write("Creating superuser...")

        create_item()

        self.stdout.write("Done.")


def create_item():
    User.objects.create_superuser("andywar65", "andy.war1965@gmail.com", "0qww294e")
