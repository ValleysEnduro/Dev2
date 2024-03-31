from django import forms
from .models import Entry
from .models import Entry, TermsandConditions

class EntryForm(forms.ModelForm):
    privacy_policy_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the privacy policy.'})
    refund_policy_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the refund policy.'})
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    terms_and_conditions_accepted = forms.BooleanField(required=True, error_messages={'required': 'I agree to the Terms and Conditions'})

    class Meta:
        model = Entry
        fields = ['first_name', 'last_name', 'date_of_birth', 'race', 'age_category', 'club_team_name', 'entry_close_datetime', 'transfer_close_datetime', 'privacy_policy_accepted','refund_policy_accepted', 'terms_and_conditions_accepted', ]


#When you want to link to this form within your templates or redirect to it in your views, you can refer to it using the namespaced URL name, like so

#<a href="{% url 'event_management:enter_race' %}">Enter a Race</a>

#Or in a view:
#return redirect('event_management:enter_race')
