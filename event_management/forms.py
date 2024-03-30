from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    privacy_policy_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the privacy policy.'})

    class Meta:
        model = Entry
        fields = ['first_name', 'last_name', 'race', 'age_category', 'club_team_name', 'entry_close_datetime', 'transfer_close_datetime', 'privacy_policy_accepted']
