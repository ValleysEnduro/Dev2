# your_app_name/factories.py
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import Venue, Event

fake = Faker()

class VenueFactory(DjangoModelFactory):
    class Meta:
        model = Venue

    name = factory.Faker('company')
    description = factory.Faker('paragraph')
    location = factory.Faker('address')
    latitude = factory.LazyFunction(lambda: fake.latitude())
    longitude = factory.LazyFunction(lambda: fake.longitude())
    # Assuming hero_image can be blank, we'll not generate images in tests to keep things simple
    # hero_image = <You could specify a method to generate test images if needed>

class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Faker('sentence', nb_words=4)
    venue = factory.SubFactory(VenueFactory)
    date = factory.Faker('future_date')
    description = factory.Faker('paragraph')
    is_completed = factory.Faker('boolean')

