from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .forms import EntryForm
from .models import Race

def create_entry(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.race = race
            entry.save()
            return redirect('event-page', event_id=race.event.id)  # Assuming you have an 'event-page' view
    else:
        form = EntryForm(initial={'race': race})
    return render(request, 'event_management/create_entry.html', {'form': form, 'race': race})# Create your views here.


from .forms import EntryForm

def entry_form_view(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a new URL
    else:
        form = EntryForm()
    return render(request, 'event_management/entry_form.html', {'form': form})
