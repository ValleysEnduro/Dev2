from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from event_management.models import Entry, Race
from payments.models import Payment, RaceEntry
from .models import CustomUser  # Import CustomUser from the current app if it's defined here

@login_required
def dashboard(request):
    user_entries = Entry.objects.filter(user=request.user).prefetch_related('related_field_if_necessary')  # Adjust as applicable
    user_race_entries = RaceEntry.objects.filter(participant=request.user).select_related('race')  # Shows races user is participating in
    user_payments = Payment.objects.filter(user=request.user).select_related('content_object')  # Adjust 'select_related' as per real relation if necessary

    context = {
        'user': request.user,
        'entries': user_entries,
        'race_entries': user_race_entries,
        'payments': user_payments,
    }
    
    return render(request, 'users/templates/dashboard.html', context)

@login_required
def cancel_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    try:
        if entry.can_cancel():
            refund = entry.refund_amount()
            entry.delete()
            messages.success(request, f"Your entry has been successfully canceled. Refund: {refund}")
        else:
            messages.error(request, "Cancellation period has passed.")
    except Exception as e:
        messages.error(request, f"Error canceling entry: {str(e)}")
    return redirect('dashboard')  # Make sure 'dashboard' is a valid named URL in your URL configuration
