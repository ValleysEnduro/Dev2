from django.urls import path
from .views import privacy_policy_view, refund_policy_view, homepage_view  # Add this line to import the views for privacy policy, refund policy, and

app_name = 'core'

urlpatterns = [
    path('', homepage_view, name='homepage'),  # Add this line
    path('privacy-policy/', privacy_policy_view, name='privacy_policy'),
    path('refund-policy/', refund_policy_view, name='refund_policy'),
]
