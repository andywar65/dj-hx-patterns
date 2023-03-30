from django.test import TestCase

from .factories import RowFactory

# from .models import Row

# from django.urls import reverse


class RowModelTest(TestCase):
    def test_row_str(self):
        row1 = RowFactory()
        self.assertEquals(row1.__str__(), row1.title)
        print("\n-Test Row title")
