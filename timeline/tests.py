from django.test import TestCase

from .factories import PhaseDelayFactory, PhaseStartFactory
from .models import Phase, get_position_by_parent, move_younger_siblings

# from django.urls import reverse


class PhaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest unmodified timeline models")
        parent = PhaseStartFactory()
        PhaseDelayFactory.create(parent=parent)
        PhaseDelayFactory.create(parent=parent, position=1)

    def test_phase_str(self):
        pha1 = Phase.objects.last()
        self.assertEquals(pha1.__str__(), pha1.title)
        print("\n-Test Phase title")

    def test_get_punctuated_index(self):
        pha1 = Phase.objects.last()
        self.assertEquals(pha1.get_punctuated_index(), "0.1")
        print("\n-Test punctuated index")

    def test_get_parent_id(self):
        pha0 = Phase.objects.first()
        pha1 = Phase.objects.last()
        self.assertEquals(pha0.get_parent_id(), None)
        self.assertEquals(pha1.get_parent_id(), pha0.id)
        print("\n-Test parent id")

    def test_get_next_previous_sibling(self):
        phases = Phase.objects.exclude(parent_id=None)
        pha0 = phases.first()
        pha1 = phases.last()
        self.assertEquals(pha0.get_next_sibling(), pha1)
        self.assertEquals(pha1.get_next_sibling(), None)
        print("\n-Test get next sibling")
        self.assertEquals(pha0.get_previous_sibling(), None)
        self.assertEquals(pha1.get_previous_sibling(), pha0)
        print("\n-Test get previous sibling")

    def test_get_position_by_parent(self):
        pha0 = Phase.objects.get(parent_id=None)
        self.assertEquals(get_position_by_parent(pha0), 2)
        self.assertEquals(get_position_by_parent(None), 1)
        print("\n-Test get position by parent")


class PhaseModifiedModelTest(TestCase):
    def setUp(cls):
        print("\nTest modified timeline models")
        parent = PhaseStartFactory()
        PhaseStartFactory.create(position=1)
        PhaseDelayFactory.create(parent=parent)
        PhaseDelayFactory.create(parent=parent, position=1)

    def test_move_down_phase(self):
        phases = Phase.objects.exclude(parent_id=None)
        pha0 = phases.first()
        pha1 = phases.last()
        title = pha1.title
        pha0.move_down()
        pha1 = Phase.objects.get(title=title)
        self.assertEquals(pha0.position, 1)
        self.assertEquals(pha1.position, 0)
        print("\n-Test move down phase")

    def test_move_up_phase(self):
        phases = Phase.objects.exclude(parent_id=None)
        pha0 = phases.first()
        pha1 = phases.last()
        title = pha0.title
        pha1.move_up()
        pha0 = Phase.objects.get(title=title)
        self.assertEquals(pha0.position, 1)
        self.assertEquals(pha1.position, 0)
        print("\n-Test move up phase")

    def test_move_younger_siblings(self):
        parent = Phase.objects.get(parent_id=None, position=0)
        pha1 = Phase.objects.get(parent_id=parent.id, position=1)
        pha2 = Phase.objects.get(parent_id=None, position=1)
        child_title = pha1.title
        title = pha2.title
        move_younger_siblings(parent, 0)
        pha1 = Phase.objects.get(title=child_title)
        self.assertEquals(pha1.position, 0)
        print("\n-Test move younger children")
        move_younger_siblings(None, 0)
        pha2 = Phase.objects.get(title=title)
        self.assertEquals(pha2.position, 0)
        print("\n-Test move younger roots")
