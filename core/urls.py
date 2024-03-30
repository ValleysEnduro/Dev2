
from django.urls import path
from .views import privacy_policy_view
from .views import refund_policy_view

urlpatterns = [
    path('privacy-policy/', privacy_policy_view, name='privacy_policy'),
    path('refund-policy/', refund_policy_view, name='refund_policy')

    # Other URLs...
]
