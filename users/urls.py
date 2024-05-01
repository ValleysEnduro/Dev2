from django.urls import path
from .views import dashboard, cancel_entry

app_name = 'users'  # Define the application namespace

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('cancel-entry/<int:entry_id>/', cancel_entry, name='cancel-entry'),
]