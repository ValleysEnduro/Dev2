from django.shortcuts import render
from .models import HomePage
from blog.models import Post  # Adjust based on your actual model import

def homepage_view(request):
    homepage_content = HomePage.objects.first()  # Fetch the first (and likely only) instance
    # Fetch some blog posts, e.g., the latest 5 posts
    posts = Post.objects.all().order_by('-created_on')[:5]
    return render(request, 'homepage.html', {'posts': posts})



