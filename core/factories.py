# In your_app_name/factories.py
import factory
from factory.django import DjangoModelFactory
from .models import RefundPolicy
import faker

fake = faker.Faker()

class RefundPolicyFactory(DjangoModelFactory):
    class Meta:
        model = RefundPolicy

    name = factory.Faker('word')  # Correct field based on your model definition
    content = factory.Faker('paragraph')
    cutoff_days = factory.Faker('random_int', min=1, max=30)
    refund_percentage = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True, min_value=1, max_value=100)
