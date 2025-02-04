from decimal import Decimal

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from kitchen.models import Cook, Dish, DishType, Ingredient


class DishViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="test_user", password="password_123_PASSWORD")
        self.client = Client()
        self.client.login(username="test_user", password="password_123_PASSWORD")

        self.dish_type = DishType.objects.create(name="Main Dish")

        self.cook = Cook.objects.create(username="cook1", password="password", first_name="John", last_name="Doe")

        self.ingredient = Ingredient.objects.create(name="Tomato")

        self.dish = Dish.objects.create(
            name="Test Dish",
            description="Test Description",
            price=10.99,
            dish_type=self.dish_type
        )

        self.dish_list_url = reverse("kitchen:dish-list")
        self.dish_detail_url = reverse("kitchen:dish-detail", args=[self.dish.pk])
        self.dish_create_url = reverse("kitchen:dish-create")
        self.dish_update_url = reverse("kitchen:dish-update", args=[self.dish.pk])
        self.dish_delete_url = reverse("kitchen:dish-delete", args=[self.dish.pk])

    def test_dish_list_view(self):
        """
        Test that DishListView displays dish list correctly
        """
        response = self.client.get(self.dish_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_list.html")
        self.assertContains(response, self.dish.name)
        self.assertQuerySetEqual(response.context["object_list"], [self.dish])

    def test_dish_list_view_search(self):
        """
        Test that DishListView filters dishes by name
        """
        Dish.objects.create(
            name="Another Dish",
            description="Description",
            price=15.99,
            dish_type=self.dish_type
        )

        response = self.client.get(self.dish_list_url + "?name=Test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Dish")
        self.assertNotContains(response, "Another Dish")

    def test_dish_detail_view(self):
        """
        Test that DishDetailView displays dish details correctly
        """
        response = self.client.get(self.dish_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_detail.html")
        self.assertContains(response, self.dish.name)
        self.assertContains(response, self.dish.description)

    def test_dish_create_view(self):
        """
        Test that DishDetailView displays dish details correctly
        """
        data = {
            "name": "New Dish",
            "description": "New Dish Description",
            "price": 20.99,
            "dish_type": self.dish_type.id,
            "cooks": [self.cook.id],
            "ingredients": [self.ingredient.id],
        }

        response = self.client.post(self.dish_create_url, data)

        self.assertEqual(response.status_code, 302)

        new_dish = Dish.objects.filter(name="New Dish").first()
        self.assertIsNotNone(new_dish)

        self.assertEqual(new_dish.description, "New Dish Description")
        self.assertEqual(new_dish.price, Decimal("20.99"))
        self.assertEqual(new_dish.dish_type, self.dish_type)
        self.assertIn(self.cook, new_dish.cooks.all())
        self.assertIn(self.ingredient, new_dish.ingredients.all())

    def test_dish_update_view(self):
        """
        Test that DishUpdateView updtes dish correctly
        """
        updated_data = {
            "name": "Updated Dish",
            "description": "Updated Description",
            "price": 12.99,
            "dish_type": self.dish_type.id,
            "cooks": [self.cook.id],
            "ingredients": [self.ingredient.id],
        }

        response = self.client.post(self.dish_update_url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dish_list_url)
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, "Updated Dish")

    def test_dish_delete_view(self):
        """
        Test that DishDeleteView delete dish correctly
        """
        response = self.client.post(self.dish_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dish_list_url)
        self.assertFalse(Dish.objects.filter(pk=self.dish.pk).exists())
