from django.test import TestCase
from django.urls import reverse

from .models import Item


class ItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest unmodified boxlist models")
        Item.objects.create(position=1, title="First")
        Item.objects.create(position=2, title="Central")
        Item.objects.create(position=3, title="Last")

    def test_item_str(self):
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


class ItemModifiedModelTest(TestCase):
    def setUp(self):
        print("\nTest modified boxlist models")
        Item.objects.create(position=1, title="First")
        Item.objects.create(position=2, title="Central")

    def test_move_up_item(self):
        it2 = Item.objects.get(title="Central")
        it2.move_up()
        it1 = Item.objects.get(title="First")
        self.assertEquals(it1.position, 2)
        print("\n-Test move up Item")

    def test_move_down_item(self):
        it1 = Item.objects.get(title="First")
        it1.move_down()
        it2 = Item.objects.get(title="Central")
        self.assertEquals(it2.position, 1)
        print("\n-Test move down Item")

    def test_move_following_items(self):
        it1 = Item.objects.get(title="First")
        it1.move_following_items()
        it2 = Item.objects.get(title="Central")
        self.assertEquals(it2.position, 1)
        print("\n-Test move following Items")


class ItemViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest unmodified boxlist views")
        Item.objects.create(position=1, title="First")
        Item.objects.create(position=2, title="Central")
        Item.objects.create(position=3, title="Last")

    def test_list_view(self):
        response = self.client.get(reverse("boxlist:list"))
        self.assertEqual(response.status_code, 200)
        print("\n-Test list status 200")
        self.assertTemplateUsed(response, "boxlist/list.html")
        print("\n-Test list template")
        response = self.client.get(
            reverse("boxlist:list"), headers={"HTTP_HX-REQUEST": True}
        )
        self.assertTemplateUsed(response, "boxlist/htmx/list.html")
        print("\n-Test list template with HTMX header")

    def test_create_view(self):
        response = self.client.get(
            reverse("boxlist:create"), headers={"HTTP_HX-REQUEST": True}
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test create status 200")
        self.assertTemplateUsed(response, "boxlist/htmx/create.html")
        print("\n-Test create template")
        response = self.client.post(
            reverse("boxlist:create"),
            {"title": "Foo"},
            headers={"HTTP_HX-REQUEST": True},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("boxlist:list"),
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test create redirect")
        it4 = Item.objects.last()
        self.assertEqual(it4.position, 4)
        print("\n-Test last created position")
