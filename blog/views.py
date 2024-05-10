from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Post
from django.core.paginator import Paginator

@require_http_methods(["GET"])
def post_list(request):
    posts = Post.objects.all().order_by('-created_on')
    
    # Adding pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

@require_http_methods(["GET"])
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})
