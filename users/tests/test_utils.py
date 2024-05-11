# users/tests/test_utils.py
from django.test import TestCase
from users.models import CustomUser
import os
from django.conf import settings

class CustomUserUtilityTest(TestCase):
    def test_custom_user_creation_without_avatar(self):
        user = CustomUser.objects.create_user(
            username='testuser_no_avatar',
            password='testpassword'
        )
        # Ensure user is created successfully
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.username, 'testuser_no_avatar')

    def test_custom_user_creation_with_email(self):
        user = CustomUser.objects.create_user(
            username='testuser_email',
            password='testpassword',
            email='testuser@example.com'
        )
        # Ensure user email is set correctly
        self.assertEqual(user.email, 'testuser@example.com')
