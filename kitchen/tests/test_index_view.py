from django.test import TestCase
from django.contrib.auth import get_user_model

from kitchen.models import Cook, Dish, DishType, Ingredient


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password_123_PASSWORD"
        )

        self.cook = Cook.objects.create_user(
            username="test_cook",
            first_name="Test",
            last_name="Cook",
            password="password_123_PASSWORD",
        )
        self.dish_type = DishType.objects.create(name="Main Course")
        self.ingredient = Ingredient.objects.create(name="Salt")
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="A test dish",
            price=9.99,
            dish_type=self.dish_type,
        )
        self.dish.ingredients.add(self.ingredient)

        self.url = "/"

    def test_redirect_if_not_logged_in(self):
        """
        Test that index view redirect to login page if user not logged in
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_view_logged_in(self):
        """
        Test that access to home page is open if user logged in
        """
        self.client.login(
            username="test_user",
            password="password_123_PASSWORD"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/index.html")

    def test_context_data(self):
        """
        Test that context data are correct:
        check the number of cooks, dishes, types of dishes, ingredients
        """
        self.client.login(
            username="test_user",
            password="password_123_PASSWORD"
        )
        response = self.client.get(self.url)

        self.assertEqual(response.context["num_cooks"], 2)
        self.assertEqual(response.context["num_dishes"], 1)
        self.assertEqual(response.context["num_dish_types"], 1)
        self.assertEqual(response.context["num_ingredients"], 1)

    def test_session_visit_counter(self):
        """
        Test that visit counter is working correctly
        """
        self.client.login(
            username="test_user",
            password="password_123_PASSWORD"
        )

        response = self.client.get(self.url)
        self.assertEqual(response.context["num_visits"], 1)

        response = self.client.get(self.url)
        self.assertEqual(response.context["num_visits"], 2)
