from django.test import TestCase
from django.urls import reverse
from event_management.tests.factories import RaceFactory, AgeCategoryFactory, EventFactory
from event_management.models import Entry
from django.utils import timezone
from datetime import timedelta

class EntryFormViewTest(TestCase):
    def setUp(self):
        self.event = EventFactory()
        self.race_within_window = RaceFactory(
            entry_close_datetime=timezone.now() + timedelta(days=1),
            transfer_close_datetime=timezone.now() + timedelta(days=1),
            event=self.event
        )
        self.race_outside_entry_window = RaceFactory(
            entry_close_datetime=timezone.now() - timedelta(days=1),
            transfer_close_datetime=timezone.now() + timedelta(days=1),
            event=self.event
        )
        self.race_outside_transfer_window = RaceFactory(
            entry_close_datetime=timezone.now() + timedelta(days=1),
            transfer_close_datetime=timezone.now() - timedelta(days=1),
            event=self.event
        )
        self.age_category = AgeCategoryFactory()

    def test_entry_form_get_request(self):
        response = self.client.get(reverse('event_management:submit_entry_form', args=[self.race_within_window.pk]))
        self.assertEqual(response.status_code, 200)

    def test_entry_closed_get_request(self):
        response = self.client.get(reverse('event_management:submit_entry_form', args=[self.race_outside_entry_window.pk]))
        self.assertEqual(response.status_code, 403)

    def test_entry_form_post_request(self):
        form_data = {
            'race': self.race_within_window.pk,
            'privacy_policy_accepted': True,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '2000-01-01',
            'email': 'test@example.com',
            'age_category': self.age_category.pk,
            'club_team_name': 'Test Club'
        }
        response = self.client.post(reverse('event_management:submit_entry_form', args=[self.race_within_window.pk]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Entry.objects.filter(first_name='Test', last_name='User').exists())

    def test_transfer_closed_get_request(self):
        response = self.client.get(reverse('event_management:submit_entry_form', args=[self.race_outside_transfer_window.pk]))
        self.assertEqual(response.status_code, 403)
