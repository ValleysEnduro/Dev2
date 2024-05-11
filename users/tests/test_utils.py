# users/tests/test_utils.py
from django.test import TestCase
from users.models import CustomUser, user_avatar_upload_to
from django.utils.text import slugify
import os

class FilePathGenerationTest(TestCase):
    def test_user_avatar_upload_to(self):
        user = CustomUser(username='testuser3')
        filename = 'test_avatar.jpg'
        expected_slug = slugify(user.username)
        expected_path = os.path.join('avatars', f'{expected_slug}.jpg')
        
        actual_path = user_avatar_upload_to(user, filename)
        
        # Verify the file path matches expected format
        self.assertEqual(actual_path, expected_path, f"Generated path {actual_path} does not match expected {expected_path}")
