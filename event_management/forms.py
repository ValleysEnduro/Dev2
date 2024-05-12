from django import forms
from .models import Entry, TermsandConditions
from django.apps import apps

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            'race', 
            'privacy_policy_accepted', 
            'refund_policy_accepted', 
            'terms_and_conditions_accepted', 
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'email', 
            'age_category', 
            'club_team_name',
        ]

        widgets = {
            'privacy_policy_accepted': forms.CheckboxInput(),
            'refund_policy_accepted': forms.CheckboxInput(),
            'terms_and_conditions_accepted': forms.CheckboxInput(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'club_team_name': forms.TextInput(attrs={'placeholder': 'Club/Team Name'}),
        }

# Custom User Creation Form
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('event_management', 'Entry')  # Dynamically reference Entry model
        fields = '__all__'

# Helper Functions
def get_entry_model():
    from .models import Entry
    return Entry

def get_terms_and_conditions_model():
    from .models import TermsandConditions
    return TermsandConditions
