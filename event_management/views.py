from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .models import Race
from .forms import EntryForm

@csrf_protect
@require_http_methods(["GET", "POST"])
def entry_form(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    # Check if the entry submission deadline has passed
    if timezone.now() > race.entry_close_datetime:
        return HttpResponseForbidden("Entry submissions are closed for this race.")
    
    # Check if the transfer submission deadline has passed
    if timezone.now() > race.transfer_close_datetime:
        return HttpResponseForbidden("Transfer submissions are closed for this race.")

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.race = race
            if request.user.is_authenticated:
                entry.user = request.user
            else:
                # For unauthenticated users, ensure their email is captured properly
                entry.user = None
            entry.save()
            return redirect('homepage')  # Redirect to a relevant page after successful form submission
        else:
            # Log form errors for debugging purposes
            print(f"Form errors: {form.errors}")
    else:
        form = EntryForm()

    context = {
        'form': form,
        'race': race
    }

    return render(request, 'event_management/entry_form.html', context)
