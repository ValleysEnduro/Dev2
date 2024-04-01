from django import forms
from .models import Entry, TermsandConditions

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
            # Add any other specific widgets if needed
        }
#When you want to link to this form within your templates or redirect to it in your views, you can refer to it using the namespaced URL name, like so

#<a href="{% url 'event_management:enter_race' %}">Enter a Race</a>

#Or in a view:
#return redirect('event_management:enter_race')


