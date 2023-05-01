from django.test import TestCase
from django.urls import reverse

from .factories import RowFactory
from .models import Row


class RowModelTest(TestCase):
    def test_row_str(self):
        row1 = RowFactory()
        self.assertEquals(row1.__str__(), row1.title)
        print("\n-Test Row title")


class RowViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest bulk table unmodified objects views")
        RowFactory.create_batch(2)

    def test_list_view(self):
        response = self.client.get(reverse("bulktable:list"))
        self.assertEqual(response.status_code, 200)
        print("\n-Test list status 200")
        self.assertTemplateUsed(response, "bulktable/list.html")
        print("\n-Test list template")
        response = self.client.get(
            reverse("bulktable:list"), headers={"hx-request": "true"}
        )
        self.assertTemplateUsed(response, "bulktable/htmx/list.html")
        print("\n-Test list template with HTMX header")

    def test_create_view(self):
        response = self.client.get(
            reverse("bulktable:create"), headers={"hx-request": "true"}
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test create status 200")
        self.assertTemplateUsed(response, "bulktable/htmx/create.html")
        print("\n-Test create template")
        response = self.client.post(
            reverse("bulktable:create"),
            {"title": "Foo", "color": "light"},
            headers={"hx-request": "true"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("bulktable:event_emit") + "?event=refreshList",
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test create redirect")


class RowModifiedViewTest(TestCase):
    def test_update_view(self):
        RowFactory.create_batch(3)
        response = self.client.get(
            reverse("bulktable:update"), headers={"hx-request": "true"}
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test update status 200")
        self.assertTemplateUsed(response, "bulktable/htmx/update.html")
        print("\n-Test update template")
        first = Row.objects.first()
        last = Row.objects.last()
        # next two responses are for coverage purposes
        response = self.client.get(
            reverse("bulktable:update") + "?ids=%(first)s" % {"first": first.id},
        )
        response = self.client.post(
            reverse("bulktable:update"),
            {"title": "Foo", "color": "success", "page": 1, "ids": [first.id]},
            headers={"hx-request": "true"},
            follow=True,
        )
        response = self.client.post(
            reverse("bulktable:update"),
            {"title": "Foo", "color": "success", "page": 1, "ids": [first.id, last.id]},
            headers={"hx-request": "true"},
            follow=True,
        )
        event = "event=refreshItem"
        self.assertRedirects(
            response,
            reverse("bulktable:event_emit")
            + "?event=refreshControllers&%(event)s%(first)s&%(event)s%(last)s"
            % {"first": str(first.id), "last": str(last.id), "event": event},
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test update redirect")
        first = Row.objects.first()
        last = Row.objects.last()
        self.assertEqual(first.color, "success")
        self.assertEqual(last.color, "success")
        print("\n-Test row color has changed")

    def test_delete_view(self):
        RowFactory.create_batch(1)
        response = self.client.get(reverse("bulktable:delete"))
        self.assertEqual(response.status_code, 404)
        print("\n-Test delete status 404")
        response = self.client.get(
            reverse("bulktable:delete"), headers={"hx-request": "true"}
        )
        self.assertEqual(response.status_code, 302)
        print("\n-Test delete status 302")
        last = Row.objects.last()
        response = self.client.get(
            reverse("bulktable:delete"),
            {"page": 2, "ids": [last.id], "number": 1},
            headers={"hx-request": "true"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("bulktable:list") + "?page=1",
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test delete redirect")
