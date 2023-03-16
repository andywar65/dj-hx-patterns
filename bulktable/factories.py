from factory import Faker
from factory.django import DjangoModelFactory

from .models import Row


class RowFactory(DjangoModelFactory):
    class Meta:
        model = Row

    title = Faker("sentence", nb_words=2)
    color = Faker("random_element", elements=[x[0] for x in Row.COLOR])
