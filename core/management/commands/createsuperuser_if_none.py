from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            username = settings.SUPERUSER_USERNAME
            email = settings.SUPERUSER_EMAIL
            password = settings.SUPERUSER_PASSWORD
            logger.info(f'Creating superuser with username: {username}')
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS('Superuser created.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
