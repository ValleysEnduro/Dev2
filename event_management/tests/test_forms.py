from django.test import TestCase
from event_management.forms import EntryForm
from event_management.models import Race, AgeCategory, Event
from datetime import date

class EntryFormTestCase(TestCase):
    
    def setUp(self):
        self.event = Event.objects.create(name='Sample Event')
        self.race = Race.objects.create(name='Sample Race', entry_fee=50.0, event=self.event)
        self.age_category = AgeCategory.objects.create(name='Adult')
    
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
