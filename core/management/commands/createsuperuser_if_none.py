from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
import logging
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = settings.SUPERUSER_USERNAME
        email = settings.SUPERUSER_EMAIL
        password = settings.SUPERUSER_PASSWORD
        
        logger.info(f'Trying to create superuser with username: {username}, email: {email}')
        
        if not User.objects.filter(is_superuser=True).exists():
            try:
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS('Superuser created.'))
                logger.info(f'Superuser created with username: {username}')
            except Exception as e:
                logger.error(f'Error creating superuser: {e}')
                self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
            logger.info('Superuser already exists.')

class Command(BaseCommand):
    help = 'List all superusers'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        superusers = User.objects.filter(is_superuser=True)
        if superusers.exists():
            for user in superusers:
                self.stdout.write(self.style.SUCCESS(f'Superuser: {user.username} ({user.email})'))
        else:
            self.stdout.write(self.style.WARNING('No superusers found'))

class Command(BaseCommand):
    help = 'Reset the superuser password'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = settings.SUPERUSER_USERNAME
        password = settings.SUPERUSER_PASSWORD
        
        try:
            user = User.objects.get(username=username, is_superuser=True)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully reset password for superuser: {username}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Superuser with username {username} does not exist'))           