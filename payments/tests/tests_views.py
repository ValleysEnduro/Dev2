from django.test import TestCase, Client
from django.urls import reverse
from payments.factories import UserFactory
from unittest.mock import patch
import json

class CreatePaymentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.create_payment_url = reverse('payments:create_payment')

    @patch('stripe.PaymentIntent.create')
    def test_create_payment_success(self, mock_create):
        mock_create.return_value = {'id': 'fake-stripe-id', 'client_secret': 'fake-client-secret'}
        self.client.force_login(self.user)
        response = self.client.post(self.create_payment_url, {'amount': 1000})
        # Use the admin login URL as a placeholder
        self.assertRedirects(response, '/')

    @patch('stripe.PaymentIntent.create', side_effect=Exception("Stripe error"))
    def test_create_payment_exception(self, mock_stripe):
        self.client.force_login(self.user)
        response = self.client.post(self.create_payment_url, {'amount': 1000})
        # Use the admin login URL as a placeholder for error redirection as well
        self.assertRedirects(response, '/')

class StripeWebhookTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.webhook_url = reverse('payments:stripe_webhook')

    @patch('stripe.Webhook.construct_event')
    def test_webhook_payment_intent_succeeded(self, mock_construct_event):
        mock_construct_event.return_value = {
            'type': 'payment_intent.succeeded',
            'data': {'object': {'id': 'some_payment_intent_id'}}
        }

        response = self.client.post(
            self.webhook_url, 
            json.dumps({'type': 'payment_intent.succeeded'}),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='dummy_signature'
        )

        self.assertEqual(response.status_code, 200)
        # No redirect here, but you could add checks for response content

# Remember, using '/admin/login/' is just for temporary testing purposes.
# Replace it with the actual URLs when you have the corresponding views and templates ready.
