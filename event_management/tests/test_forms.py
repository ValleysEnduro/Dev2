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
            'race': self.race.id,  # Ensure race field is included
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
        if response.status_code == 200:
            print("Form errors:", response.context['form'].errors if 'form' in response.context else 'No form in context')
        self.assertEqual(response.status_code, 302, f"Unexpected status code: {response.status_code}")
        self.assertRedirects(response, reverse('core:homepage'))  # Ensure correct redirect


class EntryFormFailureTest(TestCase):
    def setUp(self):
        self.race = RaceFactory()

    def test_form_submission_missing_fields(self):
        form_data = {
            'race': self.race.id,  # Ensure race field is included
            'privacy_policy_accepted': True,
            # 'refund_policy_accepted': True,  # Intentionally left out for the test
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1980-01-01',
            'email': 'john@example.com',
            'club_team_name': 'Runners Club'
        }

        response = self.client.post(reverse('event_management:submit_entry_form', args=[self.race.pk]), form_data)
        if response.status_code == 200:
            print("Form errors:", response.context['form'].errors if 'form' in response.context else 'No form in context')
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        self.assertContains(response, "This field is required.")  # Check for specific error message


class EntryFormViewTest(TestCase):
    def setUp(self):
        self.race_within_window = RaceFactory(
            entry_close_datetime=timezone.now() + timezone.timedelta(days=1),
            transfer_close_datetime=timezone.now() + timezone.timedelta(days=2)
        )

    def test_entry_form_post_request(self):
        form_data = {
            'race': self.race_within_window.id,  # Ensure race field is included
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
        if response.status_code == 200:
            print("Form errors:", response.context['form'].errors if 'form' in response.context else 'No form in context')
        self.assertEqual(response.status_code, 302, f"Unexpected status code: {response.status_code}")
        self.assertRedirects(response, reverse('core:homepage'))  # Ensure correct redirect
