from factory import Faker
from factory.django import DjangoModelFactory

from .models import Phase


class PhaseStartFactory(DjangoModelFactory):
    class Meta:
        model = Phase

    title = Faker("sentence", nb_words=2)
    phase_type = Faker("random_element", elements=[x[0] for x in Phase.TYPES])
    start = Faker("date_object")
    duration = Faker("pyint", min_value=1, max_value=10)


class PhaseDelayFactory(DjangoModelFactory):
    """Use when assignin parent"""

    class Meta:
        model = Phase

    title = Faker("sentence", nb_words=2)
    phase_type = Faker("random_element", elements=[x[0] for x in Phase.TYPES])
    duration = Faker("pyint", min_value=1, max_value=10)
    delay = Faker("pyint", min_value=-3, max_value=3)
