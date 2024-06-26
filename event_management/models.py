from django.db import models
from treebeard.mp_tree import MP_Node
from age_categories.models import AgeCategory
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from django.conf import settings
from core.models import RefundPolicy
from core.models import TermsandConditions
from django.utils import timezone
from datetime import datetime
from payments.models import Payment
from datetime import datetime, timedelta

class Venue(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    hero_image = ProcessedImageField(upload_to='venues/',
                                     processors=[ResizeToFill(1024, 768)],
                                     format='WEBP',
                                     options={'quality': 90},
                                     blank=True,
                                     null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    date = models.DateField()
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Race(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='races')
    start_time = models.TimeField()
    entry_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    age_categories = models.ManyToManyField(AgeCategory, related_name='races', blank=True)
    refund_policy = models.ForeignKey(RefundPolicy, on_delete=models.SET_NULL, null=True, blank=True, related_name='races')
    entry_close_datetime = models.DateTimeField(help_text="Deadline after which no new entries are accepted.")
    transfer_close_datetime = models.DateTimeField(help_text="Deadline after which entries cannot be transferred.")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='entries')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='entries')
    privacy_policy_accepted = models.BooleanField(default=False, verbose_name='I agree to the Privacy Policy')
    refund_policy_accepted = models.BooleanField(default=False, verbose_name='I agree to the Refund Policy')
    terms_and_conditions_accepted = models.BooleanField(default=False, verbose_name='I agree to the Terms and Conditions')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True)
    email = models.CharField(max_length=100, blank=True)
    age_category = models.ForeignKey(AgeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    club_team_name = models.CharField(max_length=100, blank=True)
    is_archived = models.BooleanField(default=False)
    entry_date = models.DateField(auto_now_add=True)
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='entry')

    def can_cancel(self):
        if not self.race.refund_policy:
            return False  # No refund policy set
        event_datetime = datetime.combine(self.race.event.date, datetime.min.time())
        event_datetime = timezone.make_aware(event_datetime, timezone.get_default_timezone())  # Make it timezone aware
        cancellation_deadline = event_datetime - timedelta(days=self.race.refund_policy.cutoff_days)
        return timezone.now() <= cancellation_deadline

    def refund_amount(self):
        if self.can_cancel():
            return self.race.entry_fee * (self.race.refund_policy.refund_percentage / 100)
        return 0