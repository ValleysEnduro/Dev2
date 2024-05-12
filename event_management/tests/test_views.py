from django.test import TestCase
from django.urls import reverse
from event_management.tests.factories import RaceFactory, UserFactory
from event_management.models import Entry
from django.utils import timezone
from datetime import timedelta

from django.urls import reverse
from django.test import TestCase
from event_management.tests.factories import RaceFactory

class EntryFormViewTest(TestCase):
    def setUp(self):
        self.race_within_window = RaceFactory()
        self.race_outside_entry_window = RaceFactory()
        self.race_outside_transfer_window = RaceFactory()

    def test_entry_form_get_request(self):
        response = self.client.get(reverse('event_management:entry_form', args=[self.race_within_window.pk]))
        self.assertEqual(response.status_code, 200)

    def test_entry_closed_get_request(self):
        response = self.client.get(reverse('event_management:entry_form', args=[self.race_outside_entry_window.pk]))
        self.assertEqual(response.status_code, 403)

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
        self.assertEqual(response.status_code, 302)  # Assuming a redirect on success

    def test_transfer_closed_get_request(self):
        response = self.client.get(reverse('event_management:entry_form', args=[self.race_outside_transfer_window.pk]))
        self.assertEqual(response.status_code, 403)
