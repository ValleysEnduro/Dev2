from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import Race
from .forms import EntryForm

# Hypothetical payment processing function
def process_payment(entry):
    # This is a mock payment process for demonstration purposes
    # In real implementation, integrate with an actual payment gateway
    try:
        # Simulate successful payment process
        return True
    except Exception as e:
        print(f"Payment error: {e}")
        return False

@require_GET
def display_entry_form(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    if timezone.now() > race.entry_close_datetime:
        return HttpResponseForbidden("Entry submissions are closed for this race.")
    
    if timezone.now() > race.transfer_close_datetime:
        return HttpResponseForbidden("Transfer submissions are closed for this race.")

    form = EntryForm()
    context = {
        'form': form,
        'race': race
    }
    return render(request, 'event_management/entry_form.html', context)

@csrf_protect
@require_POST
def submit_entry_form(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    if timezone.now() > race.entry_close_datetime:
        return HttpResponseForbidden("Entry submissions are closed for this race.")
    
    if timezone.now() > race.transfer_close_datetime:
        return HttpResponseForbidden("Transfer submissions are closed for this race.")

    form = EntryForm(request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.race = race
        if request.user.is_authenticated:
            entry.user = request.user
        else:
            entry.user = None

        # Process payment
        payment_successful = process_payment(entry)
        if payment_successful:
            entry.save()
            messages.success(request, "Your entry has been submitted successfully!")
            return redirect('core:homepage')
        else:
            messages.error(request, "Payment failed. Please try again.")
            context = {'form': form, 'race': race}
            return render(request, 'event_management/entry_form.html', context)
    else:
        print(f"Form errors: {form.errors}")
        messages.error(request, "There were errors in your form. Please correct them and try again.")
        context = {'form': form, 'race': race}
        return render(request, 'event_management/entry_form.html', context)
