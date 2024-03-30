# event_management/urls.py
from django.urls import path
from . import views

app_name = 'event_management'  # This is useful for namespacing your URLs

urlpatterns = [
    path('enter-race/', views.entry_form_view, name='enter_race'),
    # Add other URL patterns for the event_management app here...
]
