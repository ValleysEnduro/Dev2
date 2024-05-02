import sys

try:
    from users.models import Entry, Race, CustomUser
except ImportError as e:
    print("Error importing:", e, file=sys.stderr)
    print("sys.path is", sys.path, file=sys.stderr)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from event_management.models import Entry, Race  # Corrected import here
from payments.models import Payment, RaceEntry
from .models import CustomUser
from .forms import CustomUserCreationForm
import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    user_entries = Entry.objects.filter(user=request.user).prefetch_related('events')
    user_race_entries = RaceEntry.objects.filter(participant=request.user).select_related('race')
    user_payments = Payment.objects.filter(user=request.user).select_related('race_entry')

    context = {
        'user_entries': user_entries,
        'user_race_entries': user_race_entries,
        'user_payments': user_payments,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def cancel_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if entry.user != request.user:
        messages.error(request, "You do not have permission to cancel this entry.")
        return redirect('users:dashboard')
    if entry.can_cancel():
        refund = entry.refund_amount()
        entry.delete()
        messages.success(request, f"Your entry has been successfully canceled. Refund: {refund}")
    else:
        messages.error(request, "Cancellation period has passed.")
    return redirect('users:dashboard')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'users/user_login.html')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('users:login')

def register(request):
    if request.method == 'POST':
        return handle_register_post(request)
    return handle_register_get(request)

def handle_register_post(request):
    form = CustomUserCreationForm(request.POST, request.FILES)
    if form.is_valid():
        user = form.save()
        username = user.username
        messages.success(request, f'Account created for {username}!')
        return redirect('users:login')
    else:
        messages.error(request, 'There was a problem with your registration details.')
        return render(request, 'users/register.html', {'form': form})

def handle_register_get(request):
    form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def redirect_to_profile(request):
    return HttpResponseRedirect(reverse('users:profile'))
