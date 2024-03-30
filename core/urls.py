
from django.urls import path
from .views import privacy_policy_view

urlpatterns = [
    path('privacy-policy/', privacy_policy_view, name='privacy_policy'),
    # Other URLs...
]
