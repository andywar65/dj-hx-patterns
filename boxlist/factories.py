from factory import Faker
from factory.django import DjangoModelFactory

from .models import Item


class ItemFactory(DjangoModelFactory):
    class Meta:
        model = Item

    title = Faker("sentence", nb_words=2)
