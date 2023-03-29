from django.test import TestCase

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
