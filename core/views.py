from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_http_methods
from .models import HomePage, PrivacyPolicy
from blog.models import Post
from event_management.models import RefundPolicy

@require_http_methods(["GET"])
def homepage_view(request):
    # Fetch the homepage content safely
    homepage_content = HomePage.objects.first()
    if not homepage_content:
        raise Http404("No homePage content is available")
    
    # Fetch the latest 5 blog posts
    posts = Post.objects.all().order_by('-created_on')[:5]
    
    # Prepare the context for rendering
    context = {
        'homepage_content': homepage_content,
        'posts': posts
    }
    
    # Render the homepage template with context
    return render(request, 'core/homepage.html', context)

@require_http_methods(["GET"])
def privacy_policy_view(request):
    # Retrieve the current privacy policy based on slug
    policy = get_object_or_404(PrivacyPolicy, slug='current')  # Assuming 'current' identifies the active policy
    
    # Render the privacy policy template
    return render(request, 'core/privacy_policy.html', {'policy': policy})

@require_http_methods(["GET"])
def refund_policy_view(request):
    # Fetch the first RefundPolicy content
    policy = RefundPolicy.objects.first()
    if not policy:
        raise Http404("Refund policy not found")
    
    # Render the refund policy template
    return render(request, 'core/refund_policy.html', {'policy': policy})
