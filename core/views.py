from django.shortcuts import render
from .models import HomePage
from blog.models import Post  # Adjust based on your actual model import

def homepage_view(request):
    homepage_content = HomePage.objects.first()  # Assuming there's at least one HomePage instance
    posts = Post.objects.all().order_by('-created_on')[:5]
    context = {
        'homepage_content': homepage_content,  # Make sure this is correct
        'posts': posts
    }
    return render(request, 'homepage.html', context)



