import sys
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .forms import CustomUserCreationForm, AvatarForm
from event_management.models import Entry, Race
from payments.models import Payment, RaceEntry
from django.http import HttpResponseRedirect, JsonResponse

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

# View for dashboard
@login_required
@log_and_redirect
@require_GET
def dashboard(request):
    context = get_user_related_data(request.user)
    return render(request, 'users/dashboard.html', context)

# View to cancel an entry
@login_required
@log_and_redirect
@require_POST
def cancel_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    if not entry.can_cancel():
        messages.error(request, "Cancellation period has passed.")
    else:
        refund = entry.refund_amount()
        entry.delete()
        messages.success(request, f"Entry canceled. Refund: {refund}")
    return redirect('users:dashboard')

# View for user login
@require_http_methods(["GET", "POST"])
@log_and_redirect
def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': reverse('users:dashboard')})
        messages.error(request, 'Invalid username or password')
        return JsonResponse({'success': False, 'error': 'Invalid username or password'})
    return render(request, 'users/user_login.html')

# View for user profile
@login_required
@log_and_redirect
@require_GET
def profile_view(request):
    return render(request, 'users/profile.html')

# View to log out user
@require_GET
@log_and_redirect
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('users:login')

# View for user registration
@require_http_methods(["GET", "POST"])
@log_and_redirect
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return JsonResponse({'success': True, 'redirect_url': reverse('users:login')})
        messages.error(request, 'Please correct the below errors.')
        return JsonResponse({'success': False, 'error': form.errors.as_json()})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# View to redirect to profile
@login_required
@log_and_redirect
@require_GET
def redirect_to_profile(request):
    return HttpResponseRedirect(reverse('users:profile'))

# View to update user avatar
@login_required
@log_and_redirect
@require_http_methods(["GET", "POST"])
def update_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your avatar has been updated successfully!')
            return JsonResponse({'success': True, 'redirect_url': reverse('users:profile')})
        return JsonResponse({'success': False, 'error': form.errors.as_json()})
    else:
        form = AvatarForm(instance=request.user)
    return render(request, 'users/update_avatar.html', {'form': form})

# View to delete user avatar
@login_required
@log_and_redirect
@require_POST
def delete_avatar(request):
    user = request.user
    if user.avatar:
        user.avatar.delete()
        user.save()
        messages.success(request, "Avatar deleted successfully!")
    else:
        messages.error(request, "No avatar to delete.")
    return JsonResponse({'success': True, 'redirect_url': reverse('users:dashboard')})
