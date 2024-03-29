# core/views.py
from django.shortcuts import render
from .models import HomePage

def homepage_view(request):
    homepage_content = HomePage.objects.first()  # Fetch the first (and likely only) instance
    # Just use 'homepage.html' without 'core/templates/'
    return render(request, 'homepage.html', {'homepage_content': homepage_content})



