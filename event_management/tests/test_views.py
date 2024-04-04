from django.test import TestCase
from django.urls import reverse
from event_management.factories import RaceFactory, UserFactory
from event_management.models import Entry
from django.utils import timezone
from datetime import timedelta

class EntryFormViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(self.user)

        # Ensure the datetimes for the race windows are timezone-aware right at creation
        self.race_within_window = RaceFactory(
            entry_close_datetime=timezone.now() + timedelta(days=5),
            transfer_close_datetime=timezone.now() + timedelta(days=10)
        )

        self.race_outside_entry_window = RaceFactory(
            entry_close_datetime=timezone.now() - timedelta(days=1)
        )

        self.race_outside_transfer_window = RaceFactory(
            transfer_close_datetime=timezone.now() - timedelta(days=15)
        )

    def test_entry_form_get_request(self):
        response = self.client.get(reverse('event_management:entry_form', args=[self.race_within_window.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry_form.html')

    def test_entry_closed_get_request(self):
        response = self.client.get(reverse('event_management:entry_form', args=[self.race_outside_entry_window.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertIn("Entry submissions are closed", response.content.decode())

    def test_transfer_closed_get_request(self):
        response = self.client.get(reverse('event_management:entry_form', args=[self.race_outside_transfer_window.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertIn("Transfer submissions are closed", response.content.decode())

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
        response = self.client.post(reverse('event_management:entry_form', args=[self.race_within_window.pk]), form_data)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTrue(Entry.objects.filter(email='test@example.com').exists())
