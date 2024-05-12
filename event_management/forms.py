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

    def clean_privacy_policy_accepted(self):
        privacy_policy_accepted = self.cleaned_data.get('privacy_policy_accepted')
        if not privacy_policy_accepted:
            raise forms.ValidationError("You must accept the privacy policy to proceed.")
        return privacy_policy_accepted

    def clean_refund_policy_accepted(self):
        refund_policy_accepted = self.cleaned_data.get('refund_policy_accepted')
        if not refund_policy_accepted:
            raise forms.ValidationError("You must accept the refund policy to proceed.")
        return refund_policy_accepted

    def clean_terms_and_conditions_accepted(self):
        terms_and_conditions_accepted = self.cleaned_data.get('terms_and_conditions_accepted')
        if not terms_and_conditions_accepted:
            raise forms.ValidationError("You must accept the terms and conditions to proceed.")
        return terms_and_conditions_accepted
