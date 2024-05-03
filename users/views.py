import sys

try:
    from event_management.models import Entry, Race
    from users.models import CustomUser
except ImportError as e:
    print("Error importing:", e, file=sys.stderr)
    print("sys.path is", sys.path, file=sys.stderr)

import logging
from .forms import CustomUserCreationForm, AvatarForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import CustomUser
from .forms import CustomUserCreationForm
from event_management.models import Entry
from payments.models import Payment, RaceEntry
from django.http import HttpResponseRedirect
from .models import CustomUser


logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    context = {
        'user_entries': Entry.objects.filter(user=request.user).prefetch_related('events'),
        'user_race_entries': RaceEntry.objects.filter(participant=request.user).select_related('race'),
        'user_payments': Payment.objects.filter(user=request.user).select_related('race_entry'),
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def cancel_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    if not entry.can_cancel():
        messages.error(request, "Cancellation period has passed.")
    else:
        refund = entry.refund_amount()
        entry.delete()
        messages.success(request, f"Entry canceled. Refund: {refund}")
    return redirect('users:dashboard')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('users:dashboard')
        messages.error(request, 'Invalid username or password')
    return render(request, 'users/user_login.html')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('users:login')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('users:login')
        else:
            messages.error(request, 'Please correct the below errors.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def redirect_to_profile(request):
    return HttpResponseRedirect(reverse('users:profile'))

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Avatar updated successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AvatarForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})
