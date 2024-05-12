from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Race
from .forms import EntryForm

def process_payment(entry):
    try:
        print(f"Processing payment for entry ID: {entry.id}")
        return True
    except Exception as e:
        print(f"Payment error: {e}")
        return False

@require_http_methods(["GET", "POST"])
def submit_entry_form(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    if timezone.now() > race.entry_close_datetime:
        return HttpResponseForbidden("Entry submissions are closed for this race.")

    if timezone.now() > race.transfer_close_datetime:
        return HttpResponseForbidden("Transfer submissions are closed for this race.")

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.race = race
            entry.user = request.user if request.user.is_authenticated else None

            if process_payment(entry):
                entry.save()
                messages.success(request, "Your entry has been submitted successfully!")
                return redirect('core:homepage')
            else:
                messages.error(request, "Payment failed. Please try again.")
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, "There were errors in your form. Please correct them and try again.")
    else:
        form = EntryForm()

    context = {'form': form, 'race': race}
    return render(request, 'event_management/entry_form.html', context)
