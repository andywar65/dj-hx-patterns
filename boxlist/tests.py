from django.test import TestCase
from django.urls import reverse

from .models import Item, intercalate_siblings, move_down_siblings


class ItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest unmodified boxlist models")
        Item.objects.create(position=1, title="First")
        Item.objects.create(position=2, title="Central")
        Item.objects.create(position=3, title="Last")

    def test_item_str(self):
        it1 = Item.objects.get(title="First")
        self.assertEquals(it1.__str__(), "1 - First")
        print("\n-Test Item title")


class ItemModifiedModelTest(TestCase):
    def setUp(self):
        print("\nTest modified boxlist models")
        Item.objects.create(position=1, title="First")
        Item.objects.create(position=2, title="Central")
        Item.objects.create(position=3, title="Last")

    def test_move_following_items(self):
        it1 = Item.objects.get(title="First")
        it1.move_following_items()
        it2 = Item.objects.get(title="Central")
        self.assertEquals(it2.position, 1)
        print("\n-Test move following Items")

    def test_move_down_siblings(self):
        move_down_siblings(2)
        it1 = Item.objects.get(title="First")
        it2 = Item.objects.get(title="Central")
        self.assertEquals(it1.position, 1)
        self.assertEquals(it2.position, 3)
        print("\n-Test move down siblings")

    def test_intercalate_siblings_down(self):
        intercalate_siblings(2, 1)
        it2 = Item.objects.get(title="Central")
        self.assertEquals(it2.position, 1)
        print("\n-Test intercalate siblings downwards")

    def test_intercalate_siblings_up(self):
        intercalate_siblings(2, 3)
        it2 = Item.objects.get(title="Central")
        self.assertEquals(it2.position, 3)
        print("\n-Test intercalate siblings upwards")


class ItemViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest unmodified boxlist views")
        Item.objects.create(position=1, title="First")
        Item.objects.create(position=2, title="Last")

    def test_list_view(self):
        response = self.client.get(reverse("boxlist:list"))
        self.assertEqual(response.status_code, 200)
        print("\n-Test list status 200")
        self.assertTemplateUsed(response, "boxlist/list.html")
        print("\n-Test list template")
        response = self.client.get(
            reverse("boxlist:list"), headers={"hx-request": "true"}
        )
        self.assertTemplateUsed(response, "boxlist/htmx/list.html")
        print("\n-Test list template with HTMX header")

    def test_create_view(self):
        response = self.client.get(
            reverse("boxlist:create"), headers={"hx-request": "true"}
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test create status 200")
        self.assertTemplateUsed(response, "boxlist/htmx/create.html")
        print("\n-Test create template")
        it2 = Item.objects.last()
        response = self.client.post(
            reverse("boxlist:create"),
            {"title": "Foo", "target": it2.id},
            headers={"hx-request": "true"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("boxlist:list"),
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test create redirect")
        it3 = Item.objects.last()
        self.assertEqual(it3.position, 3)
        print("\n-Test last created position")


class ItemViewModifyTest(TestCase):
    def setUp(self):
        print("\nTest modified objects boxlist views")
        Item.objects.create(position=1, title="First")
        Item.objects.create(position=2, title="Last")

    def test_update_view(self):
        it1 = Item.objects.get(title="First")
        response = self.client.get(
            reverse("boxlist:update", kwargs={"pk": it1.id}),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test update status 200")
        self.assertTemplateUsed(response, "boxlist/htmx/update.html")
        print("\n-Test update template")
        response = self.client.post(
            reverse("boxlist:update", kwargs={"pk": it1.id}),
            {"title": "Bar", "target": ""},
            headers={"hx-request": "true"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("boxlist:event_emit") + "?event=refreshItem" + str(it1.id),
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test update title redirect")
        it2 = Item.objects.get(title="Last")
        response = self.client.post(
            reverse("boxlist:update", kwargs={"pk": it1.id}),
            {"title": "Goo", "target": it2.id},
            headers={"hx-request": "true"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("boxlist:event_emit") + "?event=refreshList",
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test update position redirect")
        it2 = Item.objects.get(title="Last")
        self.assertEqual(it2.position, 1)
        print("\n-Test update position")

    def test_sortable_view(self):
        it1 = Item.objects.get(title="First")
        it2 = Item.objects.get(title="Last")
        response = self.client.post(
            reverse("boxlist:sort"),
            headers={"hx-request": "false"},
        )
        self.assertEqual(response.status_code, 404)
        print("\n-Test sortable status 404")
        response = self.client.post(
            reverse("boxlist:sort"),
            {"item": [str(it2.id), str(it1.id)]},
            headers={"hx-request": "true"},
            follow=True,
        )
        string = "?event=refreshItem%(item2)s&event=refreshItem%(item1)s" % {
            "item1": str(it1.id),
            "item2": str(it2.id),
        }
        self.assertRedirects(
            response,
            reverse("boxlist:event_emit") + string,
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test sortable redirect")
        it2 = Item.objects.get(title="Last")
        self.assertEqual(it2.position, 1)
        print("\n-Test update position")

    def test_delete_view(self):
        it1 = Item.objects.get(title="First")
        response = self.client.delete(
            reverse("boxlist:update", kwargs={"pk": it1.id}),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test delete status 200")
        self.assertTemplateUsed(response, "boxlist/htmx/delete.html")
        print("\n-Test delete template")
        it2 = Item.objects.get(title="Last")
        self.assertEqual(it2.position, 1)
        print("\n-Test delete next position")
