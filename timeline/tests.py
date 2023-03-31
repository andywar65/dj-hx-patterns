# import calendar
from datetime import timedelta

from django.test import TestCase

from .factories import PhaseDelayFactory, PhaseStartFactory
from .models import Phase, get_position_by_parent, move_younger_siblings

# from django.urls import reverse


class PhaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest unmodified timeline models")
        parent = PhaseStartFactory(title="Parent")
        PhaseDelayFactory.create(parent=parent, title="First")
        PhaseDelayFactory.create(parent=parent, position=1, title="Last")

    def test_phase_str(self):
        pha1 = Phase.objects.get(title="Last")
        self.assertEquals(pha1.__str__(), "Last")
        print("\n-Test Phase title")

    def test_get_punctuated_index(self):
        pha1 = Phase.objects.get(title="Last")
        self.assertEquals(pha1.get_punctuated_index(), "0.1")
        print("\n-Test punctuated index")

    def test_get_parent_id(self):
        pha0 = Phase.objects.get(title="Parent")
        pha1 = Phase.objects.get(title="Last")
        self.assertEquals(pha0.get_parent_id(), None)
        self.assertEquals(pha1.get_parent_id(), pha0.id)
        print("\n-Test parent id")

    def test_get_next_previous_sibling(self):
        pha0 = Phase.objects.get(title="First")
        pha1 = Phase.objects.get(title="Last")
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

    def test_get_start_end(self):
        pha0 = Phase.objects.get(title="Parent")
        self.assertEquals(
            pha0.get_start_end(),
            (pha0.start, pha0.start + timedelta(days=pha0.duration * 7)),
        )
        pha1 = Phase.objects.get(title="Last")
        start = (
            pha0.start
            + timedelta(days=pha0.duration * 7)
            + timedelta(days=pha1.delay * 7)
        )
        end = start + timedelta(days=pha1.duration * 7)
        self.assertEquals(pha1.get_start_end(), (start, end))
        print("\n-Test get start_end")

    def test_get_popup(self):
        pha0 = Phase.objects.get(title="Parent")
        pha1 = Phase.objects.get(title="Last")
        start = (
            pha0.start
            + timedelta(days=pha0.duration * 7)
            + timedelta(days=pha1.delay * 7)
        )
        end = start + timedelta(days=pha1.duration * 7)
        type = pha1.get_phase_type_display()
        popup = "Type: %(type)s, start: %(start)s, end: %(end)s" % {
            "type": type,
            "start": start,
            "end": end,
        }
        self.assertEquals(pha1.get_popup(), popup)
        print("\n-Test get popup")


class PhaseModifiedModelTest(TestCase):
    def setUp(cls):
        print("\nTest modified timeline models")
        parent = PhaseStartFactory(title="Parent")
        PhaseDelayFactory.create(position=1, title="Uncle")
        PhaseDelayFactory.create(parent=parent, title="First")
        PhaseDelayFactory.create(parent=parent, position=1, title="Last")

    def test_move_down_phase(self):
        pha0 = Phase.objects.get(title="First")
        pha0.move_down()
        pha1 = Phase.objects.get(title="Last")
        self.assertEquals(pha0.position, 1)
        self.assertEquals(pha1.position, 0)
        print("\n-Test move down phase")

    def test_move_up_phase(self):
        pha1 = Phase.objects.get(title="Last")
        pha1.move_up()
        pha0 = Phase.objects.get(title="First")
        self.assertEquals(pha0.position, 1)
        self.assertEquals(pha1.position, 0)
        print("\n-Test move up phase")

    def test_move_younger_siblings(self):
        parent = Phase.objects.get(title="Parent")
        move_younger_siblings(parent, 0)
        pha1 = Phase.objects.get(title="Last")
        self.assertEquals(pha1.position, 0)
        print("\n-Test move younger children")
        move_younger_siblings(None, 0)
        pha1 = Phase.objects.get(title="Uncle")
        self.assertEquals(pha1.position, 0)
        print("\n-Test move younger roots")
