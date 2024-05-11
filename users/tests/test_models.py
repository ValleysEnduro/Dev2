from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from users.models import CustomUser, Purchase
from users.factories import CustomUserFactory, PurchaseFactory

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
        user = CustomUserFactory(groups=[group], user_permissions=[permission])
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
        self.assertTrue(user.avatar is None or not user.avatar.name)  # Check if avatar is None or has no name
