# utils.py
from django.apps import apps

def get_user_related_data(user):
    Entry = apps.get_model('event_management', 'Entry')
    Payment = apps.get_model('payments', 'Payment')

    user_entries = Entry.objects.filter(user=user).select_related('race')
    user_payments = Payment.objects.filter(user=user)

    return {
        'user_entries': user_entries,
        'user_payments': user_payments
    }
