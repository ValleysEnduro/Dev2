from django.shortcuts import render, get_object_or_404
from .models import Race
from .forms import EntryForm
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

def entry_form(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    if timezone.now() > race.entry_close_datetime:
        return HttpResponse("Entry submissions are closed for this race.", status=403)
    if timezone.now() > race.transfer_close_datetime:
        return HttpResponse("Transfer submissions are closed for this race.", status=403)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.race = race
            if request.user.is_authenticated:
                entry.user = request.user
            entry.save()
            return redirect('event-page', event_id=race.event.id)
    else:
        form = EntryForm()

    return render(request, 'entry_form.html', {'race_id': race_id})

def entry_form_view(request, race_id):
    form = EntryForm()
    return render(request, 'entry_form.html', {'form': form, 'race_id': race_id})
    