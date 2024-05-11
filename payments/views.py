import os
import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Payment, Product
from event_management.models import Race

# Set the Stripe API key globally
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = os.environ.get('STRIPE_ENDPOINT_SECRET')

@require_GET
def display_payment_form(request):
    # Simulated product retrieval for example purposes
    product = Product.objects.first()
    context = {
        'product': product,
    }
    return render(request, 'payments/create_payment.html', context)

@csrf_protect
@require_POST
def process_payment(request):
    try:
        product = Product.objects.first()
        amount = 1000  # $10.00 in cents

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method_types=['card'],
        )

        content_type = ContentType.objects.get_for_model(product)
        payment = Payment.objects.create(
            user=request.user if request.user.is_authenticated else None,
            amount=amount / 100,  # Converting cents to dollars
            stripe_payment_id=payment_intent['id'],
            status='pending',  # or other initial status
            content_type=content_type,
            object_id=product.id,
        )

        return HttpResponseRedirect(reverse('payment_page', args=[payment.id]))
    except Exception as e:
        print(f'Error creating payment: {e}')
        return HttpResponseRedirect(reverse('home'))

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print(f'Invalid payload: {e}')
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f'Invalid signature: {e}')
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    try:
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
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
        print(f'Error processing event: {e}')
        return JsonResponse({'error': 'An error occurred'}, status=500)

@require_GET
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

@require_GET
def payment_success(request):
    return HttpResponse("Payment succeeded")

@require_GET
def payment_error(request):
    return HttpResponse("Payment failed")
