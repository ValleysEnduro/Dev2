# In your_app_name/factories.py
import factory
from factory.django import DjangoModelFactory
from .models import AgeCategory

class AgeCategoryFactory(DjangoModelFactory):
    class Meta:
        model = AgeCategory

    name = factory.Sequence(lambda n: f"Category {n}")
    gender = factory.Iterator(['M', 'F'])
    min_age = factory.Faker('pyint', min_value=18, max_value=35)
    max_age = factory.LazyAttribute(lambda o: o.min_age + 5)  # Ensure max_age > min_age
