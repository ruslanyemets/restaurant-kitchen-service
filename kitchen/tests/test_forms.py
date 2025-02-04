from django.test import TestCase
from django.contrib.auth import get_user_model
from kitchen.forms import CookCreationForm, CookYearsOfExperienceUpdateForm


class CookCreationFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_cook",
            "password1": "password_123_PASSWORD",
            "password2": "password_123_PASSWORD",
            "first_name": "Test",
            "last_name": "Cook",
            "years_of_experience": 10,
        }

    def test_form_valid(self):
        """
        Test that CookCreationForm is valid
        """
        form = CookCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_form_invalid_years_of_experience(self):
        """
        Test that CookCreationForm is invalid
        if value years_of_experience > 50
        """
        self.form_data["years_of_experience"] = 60
        form = CookCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

    def test_form_invalid_years_of_experience_negative(self):
        """
        Test that CookCreationForm is invalid
        if value years_of_experience < 0
        """
        self.form_data["years_of_experience"] = -8
        form = CookCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)


class CookYearsOfExperienceUpdateFormTest(TestCase):
    def setUp(self):
        self.cook = get_user_model().objects.create_user(
            username="test_cook",
            password="password_123_PASSWORD",
            first_name="Test",
            last_name="Cook",
            years_of_experience=5,
        )

        self.valid_data = {
            "years_of_experience": 15,
        }

        self.invalid_data = {
            "years_of_experience": 60,
        }

    def test_form_valid(self):
        """
        Test that CookYearsOfExperienceUpdateForm is valid
        """
        form = CookYearsOfExperienceUpdateForm(
            data=self.valid_data,
            instance=self.cook
        )
        self.assertTrue(form.is_valid())

        form.save()
        self.cook.refresh_from_db()
        self.assertEqual(self.cook.years_of_experience, 15)

    def test_form_invalid_years_of_experience(self):
        """
        Test that CookYearsOfExperienceUpdateForm
        is invalid if value years_of_experience > 50
        """
        form = CookYearsOfExperienceUpdateForm(
            data=self.invalid_data, instance=self.cook
        )
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

    def test_form_invalid_years_of_experience_negative(self):
        """
        Test that CookYearsOfExperienceUpdateForm
        is invalid if value years_of_experience < 0
        """
        self.invalid_data["years_of_experience"] = -1
        form = CookYearsOfExperienceUpdateForm(
            data=self.invalid_data, instance=self.cook
        )
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)
