# event_management/urls.py
from django.urls import path
from . import views
from .views import EntryForm  # Import the view

app_name = 'event_management'  # This is useful for namespacing your URLs

urlpatterns = [
    path('entry_form/<int:race_id>/', views.entry_form, name='entry_form'),
    # Add other URL patterns for the event_management app here...
]
