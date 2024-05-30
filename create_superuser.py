import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wbe.settings')
django.setup()

User = get_user_model()
username = os.environ.get('SUPERUSER_USERNAME')
email = os.environ.get('SUPERUSER_EMAIL')
password = os.environ.get('SUPERUSER_PASSWORD')

if username and email and password:
    if not User.objects.filter(username=username).exists():
        print(f'Creating superuser {username}')
        User.objects.create_superuser(username=username, email=email, password=password)
else:
    print('Superuser creation skipped. Missing SUPERUSER_USERNAME, SUPERUSER_EMAIL or SUPERUSER_PASSWORD')
