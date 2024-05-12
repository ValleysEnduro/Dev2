import os
import django
from django.urls import reverse
from django.test import TestCase
from .factories import RaceFactory
from django.utils import timezone
import pytz
from event_management.models import Venue, Race, Event
from event_management.forms import EntryForm

# Explicitly setting Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'wbe.settings'
django.setup()

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
        self.assertRedirects(response, reverse('core:homepage'))
        if response.context and 'form' in response.context:
            self.assertEqual(response.context['form'].errors, {}, msg=f"Form errors: {response.context['form'].errors}")


class EntryFormFailureTest(TestCase):
    def setUp(self):
        self.venue = Venue.objects.create(
            name="Test Venue",
            description="A test venue",
            location="123 Test St, Test City",
            latitude=40.7128,
            longitude=-74.0060
        )

        self.event = Event.objects.create(
            name="Test Event",
            venue=self.venue,
            date=timezone.now().date() + timezone.timedelta(days=1),
            description="This is a test event."
        )

        self.race = Race.objects.create(
            name="Test Race",
            event=self.event,
            start_time=timezone.now().time(),
            entry_fee=50.00,
            entry_close_datetime=timezone.now() + timezone.timedelta(days=1),
            transfer_close_datetime=timezone.now() + timezone.timedelta(days=1),
            refund_policy=None
        )

    def test_form_submission_missing_fields(self):
        url = reverse('event_management:submit_entry_form', args=[self.race.id])
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context, msg="Response context is None")

        if response.context:
            form = response.context.get('form')
            self.assertIsNotNone(form, "Form is not in context")
            self.assertFalse(form.is_valid(), "Form should be invalid")
            self.assertTrue(form.errors, "Form should have errors")
            
            expected_errors = {
                'first_name': ['This field is required.'],
                'last_name': ['This field is required.'],
                'date_of_birth': ['This field is required.'],
                'privacy_policy_accepted': ['This field is required.'],
                'refund_policy_accepted': ['This field is required.'],
                'terms_and_conditions_accepted': ['This field is required.'],
            }

            for field, error in expected_errors.items():
                self.assertIn(field, form.errors)
                self.assertEqual(form.errors[field], error)



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
        self.assertRedirects(response, reverse('core:homepage'))
        if response.context and 'form' in response.context:
            self.assertEqual(response.context['form'].errors, {}, msg=f"Form errors: {response.context['form'].errors}")

