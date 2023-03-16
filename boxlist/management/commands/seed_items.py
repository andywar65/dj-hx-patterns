from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from boxlist.factories import ItemFactory
from boxlist.models import Item
from bulktable.factories import RowFactory
from hierarchy.factories import CategoryFactory
from hierarchy.models import Category


class Command(BaseCommand):
    help = "Seed database with item sample data."

    @transaction.atomic
    def handle(self, *args, **options):
        if settings.DEBUG is False:
            raise CommandError("This command cannot be run when DEBUG is False.")
        self.stdout.write("Seeding database with Items...")
        create_items()
        self.stdout.write("...Categories...")
        create_categories()
        self.stdout.write("...and Rows")
        create_rows()

        self.stdout.write("Done.")


def create_items():
    last = Item.objects.last()
    if last:
        start = last.position + 1
    else:
        start = 1
    for i in range(start, start + 10, 1):
        ItemFactory.create(position=i)


def create_categories():
    last = Category.objects.filter(parent_id=None).last()
    if last:
        start = last.position + 1
    else:
        start = 0
    for i in range(start, start + 4, 1):
        CategoryFactory.create(position=i)


def create_rows():
    RowFactory.create_batch(20)
