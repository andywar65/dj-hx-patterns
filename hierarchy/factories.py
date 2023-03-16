from factory import Faker
from factory.django import DjangoModelFactory

from .models import Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    title = Faker("sentence", nb_words=2)
