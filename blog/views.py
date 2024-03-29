from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by('-created_on')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    # Notice we're now using 'slug' instead of 'post_id'
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})
