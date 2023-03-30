from django.test import TestCase

from .models import Row

# from django.urls import reverse


class RowModelTest(TestCase):
    def setUp(self):
        print("\nTest unmodified bulk table models")
        Row.objects.create(title="Row", color="light")

    def test_category_str(self):
        row1 = Row.objects.first()
        self.assertEquals(row1.__str__(), "Row")
        print("\n-Test Row title")
