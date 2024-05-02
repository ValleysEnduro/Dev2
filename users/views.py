from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from event_management.models import Entry, Race
from payments.models import Payment, RaceEntry
from .models import CustomUser

@login_required
def dashboard(request):
    # Assuming relationships are named correctly in your models.
    # Adjust prefetch_related and select_related as per actual relationships.
    user_entries = Entry.objects.filter(user=request.user).prefetch_related('events')  # Adjust 'events' if Entry has related events.
    user_race_entries = RaceEntry.objects.filter(participant=request.user).select_related('race')
    user_payments = Payment.objects.filter(user=request.user).select_related('race_entry')  # Assuming payments link to race entries

    context = {
        'user_entries': user_entries,
        'user_race_entries': user_race_entries,
        'user_payments': user_payments,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def cancel_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
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
            login(request, user)
            return redirect('users:dashboard')  # Ensure this is the correct namespace and url name
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'users/user_login.html')  # Adjust the template name as necessary

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('users:login')

def redirect_to_profile(request):
    return HttpResponseRedirect(reverse('users:profile'))

from .forms import CustomUserCreationForm  # Ensure this import points to where your form is defined

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Handle file data
        if form.is_valid():
            user = form.save()
            username = user.username
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})