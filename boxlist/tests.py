from django.test import TestCase, override_settings

from .models import Item


@override_settings(USE_I18N=False)
class ItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest boxlist models")
        # Set up objects used by test methods
        Item.objects.create(position=1, title="First")
        Item.objects.create(position=2, title="Central")
        Item.objects.create(position=3, title="Last")

    def test_homepage_str(self):
        it1 = Item.objects.get(title="First")
        self.assertEquals(it1.__str__(), "First")
        print("\n-Test Item title")
