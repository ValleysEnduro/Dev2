# payments/tests/test_models.py
from django.test import TestCase
from payments.factories import PaymentFactory, UserFactory, ProductFactory, RaceFactory

class PaymentModelTest(TestCase):
    def test_payment_creation(self):
        user = UserFactory()
        product = ProductFactory()
        payment = PaymentFactory(user=user, content_object=product)
        self.assertTrue(payment.pk is not None)
        self.assertEqual(payment.user, user)
        self.assertEqual(payment.content_object, product)
        self.assertEqual(payment.status, 'pending')

    def test_race_entry_payment(self):
        race_entry = RaceFactory()
        payment = PaymentFactory(content_object=race_entry)
        self.assertEqual(payment.content_object, race_entry)
        # Add more tests as needed
