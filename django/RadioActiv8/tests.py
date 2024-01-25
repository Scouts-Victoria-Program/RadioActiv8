from django.test import TestCase
from .models import *


class PatrolModelTests(TestCase):
    def test_patrol_cant_check_out_without_checking_in(self):
        """
        Patrol cannot check_out() if they didn't already check_in()
        """

        base = Base(name="foo", min_patrols=0, max_patrols=0)
        base.save()

        patrol = Patrol(name="bar")
        patrol.save()

        successful_check_out = patrol.check_out(base)
        patrol.save()

        self.assertIs(successful_check_out, False)

    def test_patrol_cant_check_in_twice(self):
        """
        Patrol cannot check_in() if they didn't check_out() of last base
        """

        baseA = Base(name="foo", min_patrols=0, max_patrols=0)
        baseA.save()

        baseB = Base(name="bar", min_patrols=0, max_patrols=0)
        baseB.save()

        patrol = Patrol(name="quux")
        patrol.save()

        patrol.check_in(baseA)
        patrol.save()

        successful_check_in = patrol.check_in(baseB)
        patrol.save()

        self.assertIs(successful_check_in, False)
