from django.test import TestCase
from event_management.forms import EntryForm
from event_management.models import Entry
from event_management.factories import RaceFactory, UserFactory
import datetime

class EntryFormTest(TestCase):
    def setUp(self):
        # Using factories to create a race and a user
        self.user = UserFactory()
        self.race = RaceFactory(
            start_time=datetime.time(10, 0),
            entry_fee=25.00,
            entry_close_datetime=datetime.datetime.now() + datetime.timedelta(days=30),
            transfer_close_datetime=datetime.datetime.now() + datetime.timedelta(days=15),
        )

    def test_form_validation_and_save(self):
        # Simulating form data
        form_data = {
            'race': self.race.id,
            'privacy_policy_accepted': True,
            'refund_policy_accepted': True,
            'terms_and_conditions_accepted': True,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': datetime.date(1990, 1, 1),
            'email': 'john.doe@example.com',
            'age_category': None,  # Set to a valid ID if necessary
            'club_team_name': 'Test Team',
        }
        
        form = EntryForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Save the form with commit=False to get the instance without saving it to the DB
        entry = form.save(commit=False)
        entry.user = self.user  # Manually assign the user
        entry.save()

        # Assertions to ensure the entry was correctly saved
        saved_entry = Entry.objects.get(pk=entry.pk)  # Retrieve the saved entry from the DB
        self.assertEqual(saved_entry.first_name, 'John')
        self.assertEqual(saved_entry.last_name, 'Doe')
        self.assertEqual(saved_entry.email, 'john.doe@example.com')
        self.assertEqual(saved_entry.race, self.race)
        self.assertTrue(saved_entry.privacy_policy_accepted)
        self.assertTrue(saved_entry.refund_policy_accepted)
        self.assertTrue(saved_entry.terms_and_conditions_accepted)
