# users/tests/test_forms.py
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser
import os
from django.conf import settings

class AvatarFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_avatar_upload_via_form(self):
        # Ensure the path to your test image is correct
        avatar_path = os.path.join(settings.BASE_DIR, 'path', 'to', 'test_avatar.jpg')
        
        # Check if the file exists before proceeding with the test
        self.assertTrue(os.path.exists(avatar_path), f"Test image not found at {avatar_path}")

        with open(avatar_path, 'rb') as avatar_file:
            response = self.client.post(
                reverse('profile'),  # Replace 'profile' with your actual URL name
                {'avatar': avatar_file},
                format='multipart'
            )
        
        # Reload the user instance
        self.user.refresh_from_db()
        
        # Check if the avatar field is set
        self.assertIsNotNone(self.user.avatar, "Avatar is not set in the user model.")
        
        # Construct the expected file path
        expected_path = os.path.join(settings.MEDIA_ROOT, 'avatars', os.path.basename(self.user.avatar.name))
        
        # Log the expected path for debugging
        print(f"Expected avatar path: {expected_path}")
        
        # Verify the file exists at the expected location
        self.assertTrue(os.path.exists(expected_path), f"File not found at {expected_path}")

        # Clean up: remove the file after test
        if os.path.exists(expected_path):
            os.remove(expected_path)
