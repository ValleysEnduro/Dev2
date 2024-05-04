# utils.py
from event_management.models import Entry
from payments.models import Payment

def get_user_related_data(user):
    user_entries = Entry.objects.filter(user=user).select_related('race')
    user_payments = Payment.objects.filter(user=user)

    return {
        'user_race_entries': user_entries,
        'user_payments': user_payments
    }
