from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from kitchen.models import Ingredient


class IngredientViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password_123_PASSWORD"
        )
        self.client = Client()
        self.client.login(
            username="test_user",
            password="password_123_PASSWORD"
        )

        self.ingredient = Ingredient.objects.create(name="Test Ingredient")

        self.ingredient_list_url = reverse("kitchen:ingredient-list")
        self.ingredient_create_url = reverse("kitchen:ingredient-create")
        self.ingredient_update_url = reverse(
            "kitchen:ingredient-update", args=[self.ingredient.pk]
        )
        self.ingredient_delete_url = reverse(
            "kitchen:ingredient-delete", args=[self.ingredient.pk]
        )

    def test_ingredient_list_view(self):
        """
        Test that IngredientListView displays ingredient list correctly
        """
        response = self.client.get(self.ingredient_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/ingredient_list.html")
        self.assertContains(response, self.ingredient.name)
        self.assertQuerySetEqual(
            response.context["object_list"],
            [self.ingredient]
        )

    def test_ingredient_list_view_search(self):
        """
        Test that IngredientListView filters ingredients by name
        """
        Ingredient.objects.create(name="Another Ingredient")

        response = self.client.get(self.ingredient_list_url + "?name=Test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Ingredient")
        self.assertNotContains(response, "Another Ingredient")

    def test_ingredient_create_view(self):
        """
        Test that IngredientCreateView creates ingredient correctly
        """
        data = {"name": "New Ingredient"}

        response = self.client.post(self.ingredient_create_url, data)

        self.assertEqual(response.status_code, 302)

        new_ingredient = Ingredient.objects.filter(
            name="New Ingredient"
        ).first()
        self.assertIsNotNone(new_ingredient)
        self.assertEqual(new_ingredient.name, "New Ingredient")

    def test_ingredient_update_view(self):
        """
        Test that IngredientUpdateView updates ingredient correctly
        """
        updated_data = {"name": "Updated Ingredient"}

        response = self.client.post(self.ingredient_update_url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.ingredient_list_url)
        self.ingredient.refresh_from_db()
        self.assertEqual(self.ingredient.name, "Updated Ingredient")

    def test_ingredient_delete_view(self):
        """
        Test that IngredientDeleteView delete ingredient correctly
        """
        response = self.client.post(self.ingredient_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.ingredient_list_url)
        self.assertFalse(
            Ingredient.objects.filter(pk=self.ingredient.pk).exists()
        )
