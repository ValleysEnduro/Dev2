from django.urls import path
from . import views

urlpatterns = [
    path('core/', views.homepage_view, name='homepage'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('refund-policy/', views.refund_policy_view, name='refund_policy'),
]
