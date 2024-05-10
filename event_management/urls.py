# event_management/urls.py
from django.urls import path
from . import views

app_name = 'event_management'  # This is useful for namespacing your URLs

urlpatterns = [
    path('entry_form/<int:race_id>/', views.display_entry_form, name='display_entry_form'),
    path('submit_entry_form/<int:race_id>/', views.submit_entry_form, name='submit_entry_form'),
    # Add other URL patterns here
]
