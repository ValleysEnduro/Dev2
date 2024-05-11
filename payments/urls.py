from django.urls import path
from .views import display_payment_form, process_payment, stripe_webhook, create_entry, payment_success, payment_error

app_name = 'payments'

urlpatterns = [
    path('create/', display_payment_form, name='display_payment_form'),
    path('process/', process_payment, name='process_payment'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
    path('create_entry/<int:race_id>/', create_entry, name='create_entry'),
    path('success/', payment_success, name='payment_success'),
    path('error/', payment_error, name='payment_error'),
]
