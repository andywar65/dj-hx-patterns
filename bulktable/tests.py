from django.test import TestCase
from django.urls import reverse

from .factories import RowFactory

# from .models import Row


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
        response = self.client.get(reverse("bulktable:list"), HTTP_HX_REQUEST="true")
        self.assertTemplateUsed(response, "bulktable/htmx/list.html")
        print("\n-Test list template with HTMX header")

    def test_create_view(self):
        response = self.client.get(reverse("bulktable:create"), HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        print("\n-Test create status 200")
        self.assertTemplateUsed(response, "bulktable/htmx/create.html")
        print("\n-Test create template")
        response = self.client.post(
            reverse("bulktable:create"),
            {"title": "Foo", "color": "light"},
            HTTP_HX_REQUEST="true",
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("bulktable:add_button") + "?refresh=true",
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test create redirect")
