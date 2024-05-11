# users/views.py
import sys
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import JsonResponse, HttpResponseRedirect
from django.apps import apps
from django.middleware.csrf import get_token
from .forms import CustomUserCreationForm
from .utils import get_user_related_data

logger = logging.getLogger(__name__)

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
@require_http_methods(["GET", "POST"])
def dashboard(request):
    context = get_user_related_data(request.user)
    return render(request, 'users/dashboard.html', context)

# Separate GET and POST for cancel_entry
@login_required
@log_and_redirect
@require_GET
def confirm_cancel_entry(request, entry_id):
    Entry = apps.get_model('event_management', 'Entry')
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    return render(request, 'users/confirm_cancel.html', {'entry': entry})

@login_required
@require_POST
def cancel_entry(request, entry_id):
    Entry = apps.get_model('event_management', 'Entry')
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    if not entry.can_cancel():
        messages.error(request, "Cancellation period has passed.")
        return JsonResponse({'success': False, 'error': 'Cancellation period has passed.'})
    else:
        refund = entry.refund_amount()
        entry.delete()
        messages.success(request, f"Entry canceled. Refund: {refund}")
        return JsonResponse({'success': True})

# Separate GET and POST for login_view
@log_and_redirect
@require_GET
def login_view(request):
    return render(request, 'users/user_login.html')

@log_and_redirect
@require_POST
def perform_login(request):
    user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
    if user:
        login(request, user)
        return JsonResponse({'success': True, 'redirect_url': reverse('users:dashboard')})
    messages.error(request, 'Invalid username or password')
    return JsonResponse({'success': False, 'error': 'Invalid username or password'})

# View for user profile
@login_required
@log_and_redirect
@require_GET
def profile_view(request):
    form = CustomUserCreationForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

# Separate GET and POST for logout_view
@login_required
@log_and_redirect
@require_GET
def logout_view(request):
    return render(request, 'users/confirm_logout.html')

@login_required
@log_and_redirect
@require_POST
def perform_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return JsonResponse({'success': True, 'redirect_url': reverse('users:login')})

# Separate GET and POST for register
@log_and_redirect
@require_GET
def register_view(request):
    form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@log_and_redirect
@require_POST
def register_user(request):
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request, f'Account created for {user.username}!')
        return JsonResponse({'success': True, 'redirect_url': reverse('users:login')})
    messages.error(request, 'Please correct the below errors.')
    return JsonResponse({'success': False, 'error': form.errors.as_json()})

# View to redirect to profile
@login_required
@log_and_redirect
@require_GET
def redirect_to_profile(request):
    return HttpResponseRedirect(reverse('users:profile'))
