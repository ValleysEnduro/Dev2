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

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from event_management.models import Entry

@login_required
def cancel_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    if entry.can_cancel():
        refund = entry.refund_amount()
        entry.delete()
        messages.success(request, f"Your entry has been successfully canceled. Refund: {refund}")
    else:
        messages.error(request, "Cancellation period has passed.")
    return redirect('your-redirect-url')

from .models import PrivacyPolicy

def privacy_policy_view(request):
    policy = PrivacyPolicy.objects.latest('last_updated')
    return render(request, 'core/privacy_policy.html', {'policy': policy})



