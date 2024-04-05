from django.shortcuts import render, get_object_or_404, redirect
from .models import Race
from .forms import EntryForm
from django.http import HttpResponse
from django.utils import timezone

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
            return redirect('homepage')
    else:
        form = EntryForm()

    return render(request, 'entry_form.html', {'form': form, 'race_id': race_id})

# event_management/views.py
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from .models import Race, Entry
from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_entry(request, race_id):
    race = Race.objects.get(id=race_id)
    
    # Calculate the amount to be paid
    amount = int(race.entry_fee * 100)  # Convert to cents
    
    # Create a Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f'Entry for {race.name}',
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('entry_success', args=[race_id])) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('entry_cancel', args=[race_id])),
    )
    
    # Redirect to Stripe Checkout
    return redirect(session.url, code=303)

