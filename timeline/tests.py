import calendar
from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from .factories import PhaseDelayFactory, PhaseStartFactory
from .models import (
    Phase,
    get_chart_start_end,
    get_margin_width,
    get_month_dict,
    get_position_by_parent,
    move_younger_siblings,
)


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

    def test_get_chart_start_end(self):
        self.assertEquals(
            get_chart_start_end(2023, 1), (date(2023, 1, 1), date(2023, 12, 31))
        )
        self.assertEquals(
            get_chart_start_end(2023, 2), (date(2023, 7, 1), date(2024, 6, 30))
        )
        print("\n-Test get chart start & end")

    def test_get_margin_width(self):
        chst = date(2023, 1, 1)
        chen = date(2023, 12, 31)
        before = date(2022, 4, 13)
        andy = date(2023, 4, 13)
        mt = date(2023, 4, 23)
        after = date(2024, 4, 13)
        self.assertEquals(get_margin_width(before, before, chst, chen), (0, 0))
        self.assertEquals(get_margin_width(before, andy, chst, chen), (0, 28))
        self.assertEquals(get_margin_width(before, after, chst, chen), (0, 100))
        self.assertEquals(get_margin_width(andy, after, chst, chen), (27, 100 - 28))
        self.assertEquals(get_margin_width(andy, mt, chst, chen), (27, 3))
        self.assertEquals(get_margin_width(after, after, chst, chen), (100, 0))
        print("\n-Test margin and width")

    def test_get_month_dict(self):
        now_y = now().year
        now_m = now().month
        self.assertEquals(next(iter(get_month_dict(1999, 1))), "Jan")
        self.assertEquals(next(iter(get_month_dict(1999, 7))), "Jul")
        self.assertTrue(get_month_dict(now_y, now_m)[calendar.month_abbr[now_m]])
        print("\n-Test get month dict")

    def test_draw_bar_chart(self):
        phase = Phase.objects.create(title="Foo", start=date(2023, 4, 13))
        style = "background-color: #dddddd; margin-left: 27%; width: 2%"
        self.assertEquals(phase.draw_bar_chart(2023, 1), style)
        print("\n-Test draw bar chart")


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


class PhaseViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest unmodified objects timeline views")
        parent = PhaseStartFactory(title="Parent")
        PhaseDelayFactory.create(parent=parent, title="First")
        PhaseDelayFactory.create(parent=parent, position=1, title="Last")

    def test_list_view(self):
        response = self.client.get(
            reverse("timeline:list", kwargs={"year": 2023, "month": 1})
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test list status 200")
        self.assertTemplateUsed(response, "timeline/list.html")
        print("\n-Test list template")
        self.assertEquals(response.context["year"], 2023)
        self.assertIsInstance(response.context["month_dict"], dict)
        self.assertEquals(response.context["object_list"].first().tree_depth, 0)
        print("\n-Test list context")
        response = self.client.get(
            reverse("timeline:list", kwargs={"year": 2023, "month": 1}),
            headers={"hx-request": "true"},
        )
        self.assertTemplateUsed(response, "timeline/htmx/list.html")
        print("\n-Test list template with HTMX header")

    def test_create_view(self):
        response = self.client.get(
            reverse("timeline:create"), headers={"hx-request": "true"}
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test create status 200")
        self.assertTemplateUsed(response, "timeline/htmx/create.html")
        print("\n-Test create template")
        parent = Phase.objects.get(title="Parent")
        response = self.client.post(
            reverse("timeline:create"),
            {
                "title": "Foo",
                "parent": parent.id,
                "phase_type": "#dddddd",
                "start": "",
                "duration": 2,
                "delay": 0,
            },
            headers={"hx-request": "true"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("timeline:add_button") + "?refresh=true",
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test create redirect")
        it3 = Phase.objects.last()
        self.assertEqual(it3.position, 2)
        print("\n-Test last created position")


class PhaseViewModifyTest(TestCase):
    def setUp(self):
        print("\nTest modified objects timeline views")
        parent = PhaseStartFactory(title="Parent")
        PhaseDelayFactory.create(parent=parent, title="First")
        PhaseDelayFactory.create(parent=parent, position=1, title="Last")

    def test_update_view(self):
        ph1 = Phase.objects.get(title="First")
        response = self.client.get(
            reverse("timeline:update", kwargs={"pk": ph1.id}),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test update status 200")
        self.assertTemplateUsed(response, "timeline/htmx/update.html")
        print("\n-Test update template")
        response = self.client.post(
            reverse("timeline:update", kwargs={"pk": ph1.id}),
            {
                "title": "Bar",
                "parent": "",
                "phase_type": "#dddddd",
                "start": "",
                "duration": 2,
                "delay": 0,
            },
            headers={"hx-request": "true"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("timeline:updating", kwargs={"pk": ph1.id}),
            status_code=302,
            target_status_code=200,
        )
        print("\n-Test update redirect")

    def test_move_down_view(self):
        ph1 = Phase.objects.get(title="First")
        response = self.client.get(
            reverse("timeline:move_down", kwargs={"pk": ph1.id}),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test move down status 200")
        self.assertTemplateUsed(response, "timeline/htmx/move.html")
        print("\n-Test move down template")
        ph2 = Phase.objects.get(title="Last")
        self.assertEqual(ph2.position, 0)
        print("\n-Test move down next position")

    def test_move_up_view(self):
        ph2 = Phase.objects.get(title="Last")
        response = self.client.get(
            reverse("timeline:move_up", kwargs={"pk": ph2.id}),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test move up status 200")
        self.assertTemplateUsed(response, "timeline/htmx/move.html")
        print("\n-Test move up template")
        ph1 = Phase.objects.get(title="First")
        self.assertEqual(ph1.position, 1)
        print("\n-Test move up previous position")

    def test_delete_view(self):
        ph1 = Phase.objects.get(title="First")
        response = self.client.get(
            reverse("timeline:delete", kwargs={"pk": ph1.id}),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test delete status 200")
        self.assertTemplateUsed(response, "timeline/htmx/delete.html")
        print("\n-Test delete template")
        ph2 = Phase.objects.get(title="Last")
        self.assertEqual(ph2.position, 0)
        print("\n-Test delete next position")
