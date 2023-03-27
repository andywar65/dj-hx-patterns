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

    def test_get_next_previous_item(self):
        it1 = Item.objects.get(title="First")
        it2 = Item.objects.get(title="Central")
        it3 = Item.objects.get(title="Last")
        self.assertEquals(it1.get_next_item(), it2)
        self.assertEquals(it3.get_next_item(), None)
        self.assertEquals(it1.get_previous_item(), None)
        self.assertEquals(it3.get_previous_item(), it2)
        print("\n-Test next / previous Item")

    def test_move_up_down_item(self):
        it1 = Item.objects.get(title="First")
        it2 = Item.objects.get(title="Central")
        it2.move_up()
        self.assertEquals(it1.position, 2)
        it2.move_down()
        self.assertEquals(it1.position, 1)
        print("\n-Test move up / down Item")

    def test_move_following_items(self):
        it1 = Item.objects.get(title="First")
        it2 = Item.objects.get(title="Central")
        it1.move_following_items()
        self.assertEquals(it2.position, 1)
        print("\n-Test move following Items")
