# your_app_name/tests/test_models.py
from django.test import TestCase
from event_management.models import Venue, Event
from event_management.factories import VenueFactory, EventFactory

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
