import sys
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import CustomUserCreationForm, AvatarForm
from event_management.models import Entry, Race
from payments.models import Payment, RaceEntry
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

# Helper function to fetch common user-related data
def get_user_related_data(user):
    return {
        'user_entries': Entry.objects.filter(user=user).prefetch_related('events'),
        'user_race_entries': RaceEntry.objects.filter(participant=user).select_related('race'),
        'user_payments': Payment.objects.filter(user=user).select_related('entry'),
    }

# Decorator for common logging and redirections
def log_and_redirect(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {view_func.__name__}: {str(e)}", exc_info=sys.exc_info())
            messages.error(request, "An unexpected error occurred.")
            return redirect('users:dashboard')
    return _wrapped_view

@login_required
@log_and_redirect
def dashboard(request):
    context = get_user_related_data(request.user)
    return render(request, 'users/dashboard.html', context)

@login_required
@log_and_redirect
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
        if user:
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
        messages.error(request, 'Please correct the below errors.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def redirect_to_profile(request):
    return HttpResponseRedirect(reverse('users:profile'))

def update_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your avatar has been updated successfully!')
            return redirect('profile')  # Redirect to a relevant page
    else:
        form = AvatarForm(instance=request.user)
    
    return render(request, 'users/update_avatar.html', {'form': form})

@login_required
def delete_avatar(request):
    user = request.user
    if user.avatar:
        user.avatar.delete()  # This deletes the file and clears the field
        user.save()
        messages.success(request, "Avatar deleted successfully!")
    else:
        messages.error(request, "No avatar to delete.")
    return redirect('users:dashboard')
