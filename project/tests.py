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
    # mostly for coverage purposes
    def test_htmx_cdn_tag(self):
        out = Template("{% load htmx_tags %}{% htmx_cdn %}").render(Context())
        self.assertIn("https://unpkg.com/htmx.org@", out)
        print("\n-Test htmx cdn tag")

    def test_htmx_request_tag(self):
        request = {
            "method": "POST",
            "url": "foo",
            "target": "target",
            "include": "include",
            "swap": "none",
            "push": "true",
            "trigger": "trigger",
            "sync": "sync",
            "confirm": "confirm",
            "headers": {"foo": "bar"},
            "vals": {"foo": "bar"},
        }
        context = {"myHxReq": request}
        out = Template("{% load htmx_tags %}{% htmx_request myHxReq %}").render(
            Context(context)
        )
        self.assertIn('hx-post="foo" ', out)
        print("\n-Test htmx request tag")
