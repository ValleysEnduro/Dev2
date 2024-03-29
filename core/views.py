from django.shortcuts import render
from .models import HomePage

def homepage_view(request):
    homepage_content = HomePage.objects.first()
    return render(request, 'homepage.html', {'homepage_content': homepage_content})

