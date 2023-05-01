from django.template import Context, Template
from django.test import TestCase
from django.urls import reverse


class ProjectViewTest(TestCase):
    def test_list_view(self):
        response = self.client.get(reverse("base"))
        self.assertEqual(response.status_code, 200)
        print("\n-Test base status 200")
        self.assertTemplateUsed(response, "base.html")
        print("\n-Test base template")


class ProjectTemplateTagsTest(TestCase):
    def test_htmx_cdn_tag(self):
        out = Template("{% load htmx_tags %}" "{% htmx_cdn %}").render(Context())
        self.assertIn("https://unpkg.com/htmx.org@", out)
        print("\n-Test htmx cdn tag")
