from django import forms
from .models import Entry

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
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'club_team_name': forms.TextInput(),
        }
