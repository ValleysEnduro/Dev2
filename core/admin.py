from django.contrib import admin
from .models import HomePage

admin.site.register(HomePage)
from django.shortcuts import render
from .models import HomePage

def homepage_view(request):
    homepage_content = HomePage.objects.first()  # Assuming there's only one homepage content entry
    return render(request, 'core/homepage.html', {'homepage_content': homepage_content})

from django_summernote.admin import SummernoteModelAdmin
from .models import RefundPolicy

# Customize the admin form to use Summernote for the 'content' field
class RefundPolicyAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)  # Apply Summernote to the 'content' field
    list_display = ['name', 'cutoff_days', 'refund_percentage', 'last_updated']

admin.site.register(RefundPolicy, RefundPolicyAdmin)

from .models import PrivacyPolicy
class PrivacyPolicyAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(PrivacyPolicy)