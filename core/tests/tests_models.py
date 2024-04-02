# In your_app_name/tests/test_models.py
from django.test import TestCase
from django.utils.timezone import now
from core.factories import RefundPolicyFactory
from core.models import RefundPolicy

from django.test import TestCase
from core.models import RefundPolicy
# Ensure you have the correct import for RefundPolicyFactory
from core.factories import RefundPolicyFactory 

class RefundPolicyModelTest(TestCase):
    def test_refund_policy_creation(self):
        refund_policy = RefundPolicyFactory()

        self.assertTrue(isinstance(refund_policy, RefundPolicy))
        self.assertIsNotNone(refund_policy.name)
        self.assertGreaterEqual(refund_policy.cutoff_days, 1)
        self.assertGreaterEqual(refund_policy.refund_percentage, 1)
        self.assertLessEqual(refund_policy.refund_percentage, 100)
        self.assertTrue(refund_policy.last_updated <= now())

    def test_refund_policy_string_representation(self):
        refund_policy = RefundPolicyFactory()
        expected_string = f"Refund Policy updated on {refund_policy.last_updated.strftime('%Y-%m-%d')}"
        self.assertEqual(str(refund_policy), expected_string)
