from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    privacy_policy_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the privacy policy.'})
    refund_policy_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the refund policy.'})

    class Meta:
        model = Entry
        fields = ['first_name', 'last_name', 'race', 'age_category', 'club_team_name', 'entry_close_datetime', 'transfer_close_datetime', 'privacy_policy_accepted','refund_policy_accepted']


#When you want to link to this form within your templates or redirect to it in your views, you can refer to it using the namespaced URL name, like so

#<a href="{% url 'event_management:enter_race' %}">Enter a Race</a>

#Or in a view:
#return redirect('event_management:enter_race')
