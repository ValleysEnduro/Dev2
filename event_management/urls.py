# event_management/urls.py
from django.urls import path
from . import views

app_name = 'event_management'  # This is useful for namespacing your URLs

urlpatterns = [
    path('submit/<int:race_id>/', views.submit_entry_form, name='submit_entry_form'),
    path('entry/submit/<int:race_id>/', views.submit_entry_form, name='submit_entry_form'),
    path('race/<int:race_id>/entry/', views.submit_entry_form, name='entry_form')
]
