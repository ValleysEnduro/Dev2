# age_categories/tests/tests_models.py
from django.test import TestCase
from age_categories.models import AgeCategory  # Correct import statement
from age_categories.factories import AgeCategoryFactory  # Assuming you have this factory defined

class AgeCategoryModelTest(TestCase):
    def test_age_category_creation(self):
        age_category = AgeCategoryFactory()
        self.assertTrue(isinstance(age_category, AgeCategory))
        self.assertIsNotNone(age_category.name)
        self.assertIn(age_category.gender, ['M', 'F'])
        self.assertTrue(age_category.max_age > age_category.min_age)

    def test_age_category_string_representation(self):
        age_category = AgeCategoryFactory(name="Junior", gender="M", min_age=18, max_age=25)
        expected_str = "Junior (M) 18-25 years"
        self.assertEqual(str(age_category), expected_str)
