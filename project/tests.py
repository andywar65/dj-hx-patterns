from django.test import TestCase
from django.urls import reverse


class ProjectViewTest(TestCase):
    def test_list_view(self):
        response = self.client.get(reverse("base"))
        self.assertEqual(response.status_code, 200)
        print("\n-Test base status 200")
        self.assertTemplateUsed(response, "base.html")
        print("\n-Test base template")
        self.assertIsInstance(response.context["year"], int)
        self.assertIsInstance(response.context["month"], int)
        print("\n-Test base context")
