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
        self.assertEqual(response.status_code, 302)  # Assuming a redirect on success

class EntryFormFailureTest(TestCase):
    def setUp(self):
        self.race = RaceFactory()

    def test_form_submission_missing_fields(self):
        form_data = {
            # Intentionally omit required fields
            'first_name': 'John',
            'last_name': 'Doe',
        }

        response = self.client.post(reverse('event_management:submit_entry_form', args=[self.race.pk]), form_data)
        self.assertEqual(response.status_code, 200)  # Expecting no redirect on failure
        self.assertContains(response, 'homepage')