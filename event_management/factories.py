import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import Venue, Event, AgeCategory, RefundPolicy, Race, Entry
from django.contrib.auth import get_user_model

fake = Faker()

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

# In your_app_name/factories.py

class AgeCategoryFactory(DjangoModelFactory):
    class Meta:
        model = AgeCategory

    # Assuming AgeCategory model has a 'name' field
    name = factory.Sequence(lambda n: f"Category {n}")

class RefundPolicyFactory(DjangoModelFactory):
    class Meta:
        model = RefundPolicy

    # Assuming RefundPolicy model has fields like 'policy_name' and 'cutoff_days'
    policy_name = factory.Faker('word')
    cutoff_days = factory.Faker('random_int', min=1, max=30)

class RaceFactory(DjangoModelFactory):
    class Meta:
        model = Race

    name = factory.Faker('sentence', nb_words=4)
    event = factory.SubFactory(EventFactory)
    start_time = factory.Faker('time_object')
    # age_categories will be handled in tests, as it's a ManyToManyField
    refund_policy = factory.SubFactory(RefundPolicyFactory)
    entry_close_datetime = factory.Faker('future_datetime', end_datetime="+30d")
    transfer_close_datetime = factory.Faker('future_datetime', end_datetime="+15d")
    is_completed = factory.Faker('boolean')

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')

class EntryFactory(DjangoModelFactory):
    class Meta:
        model = Entry

    user = factory.SubFactory(UserFactory)
    race = factory.SubFactory(RaceFactory)  # Assuming you have a RaceFactory
    privacy_policy_accepted = True
    refund_policy_accepted = True
    terms_and_conditions_accepted = True
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=65)
    email = factory.Faker('email')
    age_category = None  # Set in tests if needed
    club_team_name = factory.Faker('company')