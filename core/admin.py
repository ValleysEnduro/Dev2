from django.contrib import admin
from .models import HomePage

admin.site.register(HomePage)
from django.shortcuts import render
from .models import HomePage

def homepage_view(request):
    homepage_content = HomePage.objects.first()  # Assuming there's only one homepage content entry
    return render(request, 'core/homepage.html', {'homepage_content': homepage_content})
