# users/tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from users.models import CustomUser, Purchase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.factories import CustomUserFactory, PurchaseFactory
import os
from django.conf import settings

class CustomUserTestCase(TestCase):
    def test_custom_user_creation(self):
        user = CustomUserFactory()
        self.assertIsInstance(user, CustomUser)
        self.assertTrue(user.username)
        self.assertTrue(user.email)
        self.assertTrue(user.avatar)

    def test_custom_user_with_groups_permissions(self):
        group = Group.objects.create(name='Test Group')
        permission = Permission.objects.create(
            name='Can do something',
            content_type_id=1,  # Use appropriate content type ID
            codename='can_do_something'
        )
        user = CustomUserFactory()
        user.groups.set([group])
        user.user_permissions.set([permission])
        self.assertIn(group, user.groups.all())
        self.assertIn(permission, user.user_permissions.all())

class PurchaseTestCase(TestCase):
    def test_purchase_creation(self):
        purchase = PurchaseFactory()
        self.assertIsInstance(purchase, Purchase)
        self.assertTrue(purchase.item_name)
        self.assertGreater(purchase.quantity, 0)
        self.assertIsNotNone(purchase.purchase_date)
        self.assertIsInstance(purchase.user, CustomUser)

class CustomUserEdgeCaseTestCase(TestCase):
    def test_custom_user_without_avatar(self):
        user = CustomUserFactory(avatar=None)
        self.assertTrue(user.avatar is None or user.avatar.name == '', "Avatar should be None or have no name.")

class CustomUserModelTest(TestCase):
    def test_avatar_field_handling(self):
        user = CustomUser.objects.create_user(
            username='testuser4',
            password='testpassword4'
        )
        avatar = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'fake-image-content',
            content_type='image/jpeg'
        )
        user.avatar.save('test_avatar.jpg', avatar)
        user.save()

        # Construct the expected file path
        expected_path = os.path.join(settings.MEDIA_ROOT, 'avatars', 'test_avatar.jpg')
        
        # Log the expected path for debugging
        print(f"Expected avatar path: {expected_path}")
        
        # Verify the file exists at the expected location
        self.assertTrue(os.path.exists(expected_path), f"File not found at {expected_path}")

        # Clean up
        if os.path.exists(expected_path):
            os.remove(expected_path)
