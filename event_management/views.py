from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_protect
from .models import Race
from .forms import EntryForm

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
        entry.save()
        return redirect('core:homepage')  # Updated redirect to 'core:homepage'
    else:
        print(f"Form errors: {form.errors}")
        context = {
            'form': form,
            'race': race
        }
        return render(request, 'event_management/entry_form.html', context)
