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
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertRedirects(response, reverse('homepage'))  # Ensure correct redirect

from django.test import TestCase
from django.urls import reverse
from .factories import RaceFactory

class EntryFormFailureTest(TestCase):
    def setUp(self):
        self.race = RaceFactory()

    def test_form_submission_missing_fields(self):
        form_data = {
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
        self.assertEqual(response.status_code, 200)  # Form should re-render with errors
        self.assertContains(response, "This field is required.")
