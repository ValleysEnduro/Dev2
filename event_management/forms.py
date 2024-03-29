# event_management/forms.py
from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['first_name', 'last_name', 'race', 'age_category', 'club_team_name', 'entry_close_datetime', 'transfer_close_datetime']
