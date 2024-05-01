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

from .models import PrivacyPolicy

def privacy_policy_view(request):
    policy = PrivacyPolicy.objects.latest('last_updated')
    return render(request, 'core/privacy_policy.html', {'policy': policy})

from event_management.models import RefundPolicy

def refund_policy_view(request):
    policy = RefundPolicy.objects.first()  # Assuming you have a single refund policy
    return render(request, 'core/refund_policy.html', {'policy': policy})



