# your_app_name/tests/test_models.py
from django.test import TestCase
from event_management.models import Venue, Event, Race, Entry
from event_management.factories import VenueFactory, EventFactory, RaceFactory, EntryFactory

class VenueModelTest(TestCase):
    def test_venue_creation(self):
        # Create a venue instance using the factory
        venue = VenueFactory()

        # Verify the venue was created and has expected attributes
        self.assertIsNotNone(venue.name)
        self.assertIsNotNone(venue.location)
        # Add more assertions as needed based on your model's logic and fields

    def test_venue_string_representation(self):
        # Create a venue with a specific name
        venue_name = "Test Venue"
        venue = VenueFactory(name=venue_name)

        # Verify the __str__ method returns the venue's name
        self.assertEqual(str(venue), venue_name)

# Add more tests to cover specific behaviors or methods of your Venue model

class EventModelTest(TestCase):
    def test_event_creation(self):
        event = EventFactory()
        self.assertIsNotNone(event.name)
        self.assertTrue(isinstance(event.venue, Venue))

    def test_event_string_representation(self):
        event_name = "Test Event"
        event = EventFactory(name=event_name)
        self.assertEqual(str(event), event_name)

# event_management/tests/test_models.py
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

class EntryModelTest(TestCase):
    def test_entry_creation(self):
        entry = EntryFactory()

        self.assertTrue(entry.privacy_policy_accepted)
        self.assertTrue(entry.refund_policy_accepted)
        self.assertTrue(entry.terms_and_conditions_accepted)
        self.assertIsNotNone(entry.first_name)
        self.assertIsNotNone(entry.last_name)
        self.assertIsNotNone(entry.email)
        self.assertFalse(entry.is_archived)

    def test_entry_can_cancel(self):
        race = RaceFactory(event__date=timezone.now() + timedelta(days=30),
                           refund_policy__cutoff_days=10)
        entry = EntryFactory(race=race)

        self.assertTrue(entry.can_cancel())

    def test_entry_refund_amount(self):
        race = RaceFactory(event__date=timezone.now() + timedelta(days=30),
                           refund_policy__cutoff_days=10,
                           refund_policy__refund_percentage=75)
        entry = EntryFactory(race=race)

        self.assertEqual(entry.refund_amount(), 0)  # Adjust based on your model's logic
