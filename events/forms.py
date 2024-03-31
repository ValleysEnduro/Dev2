# events/forms.py
from django import forms
from .models import Participant

class EntryForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'team', 'age_category']  # Customize fields as needed
