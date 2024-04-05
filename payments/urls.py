# payments/urls.py
from django.urls import path
from .views import create_payment, stripe_webhook

app_name = 'payments'

urlpatterns = [
    path('create/', create_payment, name='create_payment'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
]

from django.urls import path
from . import views

urlpatterns = [
    # your other url patterns
    path('success/', views.payment_success, name='payment_success'),
    path('error/', views.payment_error, name='payment_error'),
]
