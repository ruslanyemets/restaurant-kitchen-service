from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from kitchen.models import DishType


class DishTypeViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password_123_PASSWORD"
        )
        self.client = Client()
        self.client.login(
            username="test_user",
            password="password_123_PASSWORD"
        )

        self.dish_type = DishType.objects.create(name="Test Dish Type")

        self.dish_type_list_url = reverse("kitchen:dish-type-list")
        self.dish_type_create_url = reverse("kitchen:dish-type-create")
        self.dish_type_update_url = reverse(
            "kitchen:dish-type-update", args=[self.dish_type.pk]
        )
        self.dish_type_delete_url = reverse(
            "kitchen:dish-type-delete", args=[self.dish_type.pk]
        )

    def test_dish_type_list_view(self):
        """
        Test that DishTypeListView displays dish types list correctly
        """
        response = self.client.get(self.dish_type_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")
        self.assertContains(response, self.dish_type.name)
        self.assertQuerySetEqual(
            response.context["object_list"],
            [self.dish_type]
        )

    def test_dish_type_list_view_search(self):
        """
        Test that DishTypeListView filters dish types by name
        """
        DishType.objects.create(name="Another Dish Type")

        response = self.client.get(self.dish_type_list_url + "?name=Test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Dish Type")
        self.assertNotContains(response, "Another Dish Type")

    def test_dish_type_create_view(self):
        """
        Test that DishTypeCreateView creates dish type correctly
        """
        data = {"name": "New Dish Type"}

        response = self.client.post(self.dish_type_create_url, data)

        self.assertEqual(response.status_code, 302)

        new_dish_type = DishType.objects.filter(name="New Dish Type").first()
        self.assertIsNotNone(new_dish_type)
        self.assertEqual(new_dish_type.name, "New Dish Type")

    def test_dish_type_update_view(self):
        """
        Test that DishTypeUpdateView updates dish type correctly
        """
        updated_data = {"name": "Updated Dish Type"}

        response = self.client.post(self.dish_type_update_url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dish_type_list_url)
        self.dish_type.refresh_from_db()
        self.assertEqual(self.dish_type.name, "Updated Dish Type")

    def test_dish_type_delete_view(self):
        """
        Test that DishTypeDeleteView delete dish type correctly
        """
        response = self.client.post(self.dish_type_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dish_type_list_url)
        self.assertFalse(
            DishType.objects.filter(pk=self.dish_type.pk).exists()
        )
