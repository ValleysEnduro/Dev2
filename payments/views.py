from django.shortcuts import render, redirect
from django.conf import settings
from .models import Payment
import stripe
# In payments/views.py
from event_management.models import Race, Entry
from django.urls import reverse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from .models import Payment, Product, RaceEntry



stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment(request, *args, **kwargs):
    if request.method == 'POST':
        # Simulated product or associated object retrieval/creation
        product = Product.objects.first()  # Simplified for example purposes
        amount = 1000  # $10.00 in cents
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card'],
            )
            content_type = ContentType.objects.get_for_model(product)
            payment = Payment.objects.create(
                user=request.user,
                amount=amount / 100,  # Converting cents to dollars
                stripe_payment_id=payment_intent['id'],
                status='pending',  # or other initial status
                content_type=content_type,
                object_id=product.id,
            )
            # Redirect to a page where the user can complete the payment
            return HttpResponseRedirect(reverse('payment_page', args=[payment.id]))  # Adjust the URL name as necessary
        except Exception as e:
            # Handle the error by redirecting to a generic error handling view or URL
            return HttpResponseRedirect(reverse('home'))  # Use an existing URL as a fallback
    # Render your payment form template if GET request
    return render(request, 'payments/create_payment.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'your_endpoint_secret'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        # Update your Payment model based on Stripe's payment intent ID
        # e.g., mark the payment as completed
    # ... handle other event types

    return HttpResponse(status=200)

# event_management/views.py


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


