from django.test import TestCase
from django.urls import reverse
from event_management.factories import RaceFactory, UserFactory
from event_management.models import Entry, Race
from django.utils import timezone
from datetime import timedelta

class EntryFormViewTest(TestCase):
    def setUp(self):
        # Creating a user
        self.user = UserFactory()
        self.client.force_login(self.user)

        # Creating a race within the entry and transfer window
        self.race_within_window = RaceFactory(
            entry_close_datetime=timezone.now() + timedelta(days=5),
            transfer_close_datetime=timezone.now() + timedelta(days=10)
        )

        # Creating a race outside the entry window
        self.race_outside_entry_window = RaceFactory(
            entry_close_datetime=timezone.now() - timedelta(days=1)
        )

        # Creating a race outside the transfer window
        self.race_outside_transfer_window = RaceFactory(
            entry_close_datetime=timezone.now() + timedelta(days=5),
            transfer_close_datetime=timezone.now() - timedelta(days=1)
        )

    def test_entry_form_get_request(self):
        """Test that the entry form page loads correctly."""
        response = self.client.get(reverse('event_management:entry_form', args=[self.race_within_window.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry_form.html')

    def test_entry_closed_get_request(self):
        """Test accessing a race that's closed for entry submissions."""
        response = self.client.get(reverse('event_management:entry_form', args=[self.race_outside_entry_window.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b"Entry submissions are closed for this race.")

    def test_transfer_closed_get_request(self):
        """Test accessing a race that's closed for transfer submissions."""
        response = self.client.get(reverse('event_management:entry_form', args=[self.race_outside_transfer_window.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b"Transfer submissions are closed for this race.")

    def test_entry_form_post_request(self):
        """Test submitting the entry form successfully."""
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
        
        # Assuming you redirect to a 'homepage' or similar after successful form submission
        self.assertRedirects(response, reverse('homepage'))
        self.assertTrue(Entry.objects.filter(email='test@example.com').exists())
