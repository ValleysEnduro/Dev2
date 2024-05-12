# payments/factories.py
import factory
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from .models import Payment, Product
from event_management.models import Race, Entry
import faker
from event_management.tests.factories import RaceFactory


fake = faker.Faker()

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')

class RaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Race

    name = factory.Faker('sentence', nb_words=6)
    start_time = factory.LazyFunction(fake.date_time_this_decade)
    entry_fee = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=4, right_digits=2, positive=True))

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    price = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=5, right_digits=2, positive=True))

class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory(UserFactory)
    amount = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=5, right_digits=2, positive=True))
    status = factory.Iterator(['pending', 'completed', 'failed'])
    stripe_payment_id = factory.Faker('uuid4')

    @factory.post_generation
    def set_content_object(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.content_object = extracted
            self.save()

# Adjustments to tests
from django.test import TestCase
from .factories import PaymentFactory, ProductFactory
from event_management.tests.factories import RaceFactory, EntryFactory

class PaymentModelTest(TestCase):

    def test_payment_creation_with_product(self):
        product = ProductFactory()
        payment = PaymentFactory(content_object=product)
        
        self.assertEqual(payment.content_object, product)

    def test_payment_creation_with_race_entry(self):
        entry = EntryFactory()
        payment = PaymentFactory(content_object=entry)
        
        self.assertEqual(payment.content_object, entry)

    def test_payment_creation_with_race(self):
        race = RaceFactory()
        payment = PaymentFactory(content_object=race)
        
        self.assertEqual(payment.content_object, race)

    def test_payment_statuses(self):
        payment_pending = PaymentFactory(status='pending')
        payment_completed = PaymentFactory(status='completed')
        payment_failed = PaymentFactory(status='failed')

        self.assertEqual(payment_pending.status, 'pending')
        self.assertEqual(payment_completed.status, 'completed')
        self.assertEqual(payment_failed.status, 'failed')
