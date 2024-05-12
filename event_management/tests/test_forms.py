import django
django.setup()

from django.urls import reverse
from django.test import TestCase
from .factories import RaceFactory
from django.utils import timezone
import pytz

class EntryFormTimezoneTest(TestCase):
    def setUp(self):
        self.race = RaceFactory()

    def test_form_submission_different_timezone(self):
        form_data = {
            'race': self.race.id,
            'privacy_policy_accepted': True,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'email': 'john@example.com',
            'club_team_name': 'Runners Club'
        }

        user_timezone = pytz.timezone('Asia/Tokyo')
        timezone.activate(user_timezone)

        response = self.client.post(reverse('event_management:submit_entry_form', args=[self.race.pk]), form_data)
        self.assertEqual(response.status_code, 302)
        if response.context and 'form' in response.context:
            self.assertEqual(response.context['form'].errors, {}, msg=f"Form errors: {response.context['form'].errors}")
        self.assertRedirects(response, reverse('core:homepage'))

class EntryFormFailureTest(TestCase):
    def setUp(self):
        self.race = RaceFactory()

    def test_form_submission_missing_fields(self):
        form_data = {
            'race': self.race.id,
            'privacy_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'email': 'john@example.com',
            'club_team_name': 'Runners Club'
        }

        response = self.client.post(reverse('event_management:submit_entry_form', args=[self.race.pk]), form_data)

        # Ensure redirection happens
        self.assertEqual(response.status_code, 302)

        # Follow the redirection
        follow_response = self.client.get(response.url)

        # Check the final status code
        self.assertEqual(follow_response.status_code, 200)

        # Debugging: Print response content and errors
        print(f"Redirection URL: {response.url}")
        print(f"Response Content: {follow_response.content.decode('utf-8')}")
        
        # Check if context is available and contains form errors
        if follow_response.context is not None:
            if 'form' in follow_response.context:
                form_errors = follow_response.context['form'].errors.get('refund_policy_accepted', [])
                self.assertIn("This field is required.", form_errors)
            else:
                self.fail("Form is not present in the context.")
        else:
            self.fail("Context is None after redirection.")


class EntryFormViewTest(TestCase):
    def setUp(self):
        self.race_within_window = RaceFactory(
            entry_close_datetime=timezone.now() + timezone.timedelta(days=1),
            transfer_close_datetime=timezone.now() + timezone.timedelta(days=2)
        )

    def test_entry_form_post_request(self):
        form_data = {
            'race': self.race_within_window.id,
            'privacy_policy_accepted': True,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '2000-01-01',
            'email': 'test@example.com',
            'club_team_name': 'Test Club'
        }

        response = self.client.post(reverse('event_management:submit_entry_form', args=[self.race_within_window.pk]), form_data)
        self.assertEqual(response.status_code, 302)
        if response.context and 'form' in response.context:
            self.assertEqual(response.context['form'].errors, {}, msg=f"Form errors: {response.context['form'].errors}")
        self.assertRedirects(response, reverse('core:homepage'))
