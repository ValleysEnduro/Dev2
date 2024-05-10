import os
import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Payment, Product, RaceEntry
from event_management.models import Race

# Set the Stripe API key globally
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = os.environ.get('STRIPE_ENDPOINT_SECRET')

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
            # Log the error and redirect to a generic error handling view or URL
            print(f'Error creating payment: {e}')
            return HttpResponseRedirect(reverse('home'))  # Use an existing URL as a fallback
    # Render your payment form template if GET request
    return render(request, 'payments/create_payment.html')

@require_POST
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(f'Invalid payload: {e}')
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f'Invalid signature: {e}')
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle the event
    try:
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            # Update your Payment model based on Stripe's payment intent ID
            payment = Payment.objects.filter(stripe_payment_id=payment_intent['id']).first()
            if payment:
                payment.status = 'completed'
                payment.save()
                print(f'PaymentIntent {payment_intent["id"]} succeeded.')
            else:
                print(f'PaymentIntent {payment_intent["id"]} not found in database.')
        else:
            print(f'Unhandled event type: {event["type"]}')

        return JsonResponse({'status': 'success'})
    except Exception as e:
        # Log the error
        print(f'Error processing event: {e}')
        return JsonResponse({'error': 'An error occurred'}, status=500)

def create_entry(request, race_id):
    race = Race.objects.get(id=race_id)
    amount = int(race.entry_fee * 100)  # Convert to cents

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

    return redirect(session.url, code=303)

def payment_success(request):
    return HttpResponse("Payment succeeded")

def payment_error(request):
    return HttpResponse("Payment failed")
