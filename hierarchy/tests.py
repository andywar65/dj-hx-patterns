from django.test import TestCase
from django.urls import reverse

from .models import Category, get_position_by_parent, move_younger_siblings

# from django.urls import reverse


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest unmodified hierarchy models")
        parent = Category.objects.create(title="Parent")
        Category.objects.create(title="Uncle", position=1)
        Category.objects.create(title="First", parent=parent)
        Category.objects.create(position=1, title="Last", parent=parent)

    def test_category_str(self):
        cat1 = Category.objects.get(title="First")
        self.assertEquals(cat1.__str__(), "First")
        print("\n-Test Category title")

    def test_get_punctuated_index(self):
        cat1 = Category.objects.get(title="First")
        self.assertEquals(cat1.get_punctuated_index(), "0.0")
        print("\n-Test punctuated index")

    def test_get_parent_id(self):
        cat0 = Category.objects.get(title="Parent")
        cat1 = Category.objects.get(title="First")
        self.assertEquals(cat0.get_parent_id(), None)
        self.assertEquals(cat1.get_parent_id(), cat0.id)
        print("\n-Test parent id")

    def test_get_next_previous_sibling(self):
        cat0 = Category.objects.get(title="First")
        cat1 = Category.objects.get(title="Last")
        self.assertEquals(cat0.get_next_sibling(), cat1)
        self.assertEquals(cat1.get_next_sibling(), None)
        print("\n-Test get next sibling")
        self.assertEquals(cat0.get_previous_sibling(), None)
        self.assertEquals(cat1.get_previous_sibling(), cat0)
        print("\n-Test get previous sibling")

    def test_get_position_by_parent(self):
        cat0 = Category.objects.get(title="Parent")
        self.assertEquals(get_position_by_parent(cat0), 2)
        self.assertEquals(get_position_by_parent(None), 2)
        print("\n-Test get position by parent")


class CategoryModifiedModelTest(TestCase):
    def setUp(cls):
        print("\nTest modified hierarchy models")
        parent = Category.objects.create(title="Parent")
        Category.objects.create(title="Uncle", position=1)
        Category.objects.create(title="First", parent=parent)
        Category.objects.create(title="Last", parent=parent, position=1)

    def test_move_down_category(self):
        cat0 = Category.objects.get(title="First")
        cat0.move_down()
        cat1 = Category.objects.get(title="Last")
        self.assertEquals(cat0.position, 1)
        self.assertEquals(cat1.position, 0)
        print("\n-Test move down category")

    def test_move_up_category(self):
        cat1 = Category.objects.get(title="Last")
        cat1.move_up()
        cat0 = Category.objects.get(title="First")
        self.assertEquals(cat0.position, 1)
        self.assertEquals(cat1.position, 0)
        print("\n-Test move up category")

    def test_move_younger_siblings(self):
        parent = Category.objects.get(title="Parent")
        move_younger_siblings(parent, 0)
        cat1 = Category.objects.get(title="Last")
        self.assertEquals(cat1.position, 0)
        print("\n-Test move younger children")
        move_younger_siblings(None, 0)
        cat1 = Category.objects.get(title="Uncle")
        self.assertEquals(cat1.position, 0)
        print("\n-Test move younger roots")


class CategoryViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest unmodified objects hierarchy views")
        parent = Category.objects.create(title="Parent")
        Category.objects.create(parent=parent, title="First")
        Category.objects.create(parent=parent, position=1, title="Last")

    def test_list_view(self):
        response = self.client.get(reverse("hierarchy:list"))
        self.assertEqual(response.status_code, 200)
        print("\n-Test list status 200")
        self.assertTemplateUsed(response, "hierarchy/list.html")
        print("\n-Test list template")
        self.assertEquals(response.context["object_list"].first().tree_depth, 0)
        print("\n-Test list context")
        response = self.client.get(
            reverse("hierarchy:list"), headers={"hx-request": "true"}
        )
        self.assertTemplateUsed(response, "hierarchy/htmx/list.html")
        print("\n-Test list template with HTMX header")

    def test_create_view(self):
        response = self.client.get(
            reverse("hierarchy:create"), headers={"hx-request": "true"}
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test create status 200")
        self.assertTemplateUsed(response, "hierarchy/htmx/create.html")
        print("\n-Test create template")
        parent = Category.objects.get(title="Parent")
        response = self.client.post(
            reverse("hierarchy:create"),
            {
                "title": "Foo",
                "parent": parent.id,
            },
            headers={"hx-request": "true"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("hierarchy:list"),
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test create redirect")
        cat3 = Category.objects.last()
        self.assertEqual(cat3.position, 2)
        print("\n-Test last created position")


class CategoryViewModifyTest(TestCase):
    def setUp(self):
        print("\nTest modified objects hierarchy views")
        parent = Category.objects.create(title="Parent")
        Category.objects.create(parent=parent, title="First")
        Category.objects.create(parent=parent, position=1, title="Last")

    def test_update_view(self):
        parent = Category.objects.get(title="Parent")
        cat1 = Category.objects.get(title="First")
        response = self.client.get(
            reverse("hierarchy:update", kwargs={"pk": cat1.id}),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test update status 200")
        self.assertTemplateUsed(response, "hierarchy/htmx/update.html")
        print("\n-Test update template")
        response = self.client.post(
            reverse("hierarchy:update", kwargs={"pk": cat1.id}),
            {
                "title": "Bar",
                "parent": parent.id,
            },
            headers={"hx-request": "true"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("hierarchy:detail", kwargs={"pk": cat1.id}),
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test update redirect")
        response = self.client.post(
            reverse("hierarchy:update", kwargs={"pk": cat1.id}),
            {
                "title": "Bar",
                "parent": "",
            },
            headers={"hx-request": "true"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("hierarchy:detail", kwargs={"pk": cat1.id}) + "?refresh=true",
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test update refresh redirect")

    def test_move_down_view(self):
        cat1 = Category.objects.get(title="First")
        response = self.client.get(
            reverse("hierarchy:move_down", kwargs={"pk": cat1.id}),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 302)
        print("\n-Test move down status 302")
        self.assertRedirects(
            response,
            reverse("hierarchy:list"),
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test move down next redirects")
        cat2 = Category.objects.get(title="Last")
        self.assertEqual(cat2.position, 0)
        print("\n-Test move down next position")

    def test_move_up_view(self):
        cat2 = Category.objects.get(title="Last")
        response = self.client.get(
            reverse("hierarchy:move_up", kwargs={"pk": cat2.id}),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 302)
        print("\n-Test move up status 302")
        self.assertRedirects(
            response,
            reverse("hierarchy:list"),
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test move up next redirects")
        cat1 = Category.objects.get(title="First")
        self.assertEqual(cat1.position, 1)
        print("\n-Test move up previous position")

    def test_delete_view(self):
        cat1 = Category.objects.get(title="First")
        response = self.client.get(
            reverse("hierarchy:delete", kwargs={"pk": cat1.id}),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test delete status 200")
        self.assertTemplateUsed(response, "hierarchy/htmx/delete.html")
        print("\n-Test delete template")
        cat2 = Category.objects.get(title="Last")
        self.assertEqual(cat2.position, 0)
        print("\n-Test delete next position")
