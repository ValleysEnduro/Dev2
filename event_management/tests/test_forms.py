from django.test import TestCase
from event_management.forms import EntryForm
from event_management.models import Race, AgeCategory, Event, Venue
from datetime import date

class EntryFormTestCase(TestCase):

    def setUp(self):
        self.venue = Venue.objects.create(name='Sample Venue', address='1234 Sample St')
        self.event = Event.objects.create(
            name='Sample Event',
            date=date.today() + timedelta(days=30),  # Ensure a future date
            venue=self.venue  # Set venue
        )
        self.race = Race.objects.create(
            name='Sample Race', 
            entry_fee=50.0, 
            event=self.event
        )
        self.age_category = AgeCategory.objects.create(
            name='Adult',
            min_age=18,  # Provide required min_age
            max_age=99   # Provide required max_age
        )

    def test_form_valid_data(self):
        form_data = {
            'race': self.race.id,
            'privacy_policy_accepted': True,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'email': 'john.doe@example.com',
            'age_category': self.age_category.id,
            'club_team_name': 'Sample Club',
        }
        form = EntryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_required_fields(self):
        form_data = {
            'race': self.race.id,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
        }
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('privacy_policy_accepted', form.errors)

    def test_form_missing_non_required_fields(self):
        form_data = {
            'race': self.race.id,
            'privacy_policy_accepted': True,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
        }
        form = EntryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_date_format(self):
        form_data = {
            'race': self.race.id,
            'privacy_policy_accepted': True,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '01-01-1990',  # Incorrect format
        }
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date_of_birth', form.errors)

    def test_form_empty_required_checkbox(self):
        form_data = {
            'race': self.race.id,
            'privacy_policy_accepted': False,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
        }
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('privacy_policy_accepted', form.errors)

    def test_form_invalid_email(self):
        form_data = {
            'race': self.race.id,
            'privacy_policy_accepted': True,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'email': 'invalid-email',  # Invalid email format
        }
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_future_date_of_birth(self):
        future_date = date.today().replace(year=date.today().year + 1).isoformat()
        form_data = {
            'race': self.race.id,
            'privacy_policy_accepted': True,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': future_date,  # Future date
        }
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date_of_birth', form.errors)

    def test_form_invalid_age_category(self):
        form_data = {
            'race': self.race.id,
            'privacy_policy_accepted': True,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'age_category': 9999,  # Non-existing age category
        }
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('age_category', form.errors)

from django.test import TestCase
from django.urls import reverse
from event_management.tests.factories import RaceFactory, AgeCategoryFactory, EventFactory
from event_management.models import Entry
from django.utils import timezone
from datetime import timedelta, date

class EntryFormViewTest(TestCase):
    def setUp(self):
        self.event = EventFactory(date=date.today() + timedelta(days=30))  # Ensure a future date
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
        self.age_category = AgeCategoryFactory(
            min_age=18,  # Provide required min_age
            max_age=99   # Provide required max_age
        )

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
