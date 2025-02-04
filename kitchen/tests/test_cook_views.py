from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from kitchen.models import Cook


class CookViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password_123_PASSWORD"
        )

        self.cook_1 = Cook.objects.create(
            username="cook1",
            first_name="John",
            last_name="Doe",
            years_of_experience=5
        )
        self.cook_2 = Cook.objects.create(
            username="cook2",
            first_name="Jane",
            last_name="Smith",
            years_of_experience=3
        )

        self.list_url = reverse("kitchen:cook-list")
        self.create_url = reverse("kitchen:cook-create")
        self.update_url = reverse(
            "kitchen:cook-update",
            kwargs={"pk": self.cook_1.pk}
        )
        self.delete_url = reverse(
            "kitchen:cook-delete",
            kwargs={"pk": self.cook_1.pk}
        )

        self.cook_data = {
            "username": "new_cook",
            "password1": "password_123_PASSWORD",
            "password2": "password_123_PASSWORD",
            "first_name": "New",
            "last_name": "Cook",
            "years_of_experience": 4,
        }

        self.client.login(username="test_user", password="password_123_PASSWORD")

    def test_cook_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_list.html")
        self.assertEqual(len(response.context["cook_list"]), 3)

    def test_cook_detail_view(self):
        response = self.client.get(reverse("kitchen:cook-detail", kwargs={"pk": self.cook_1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_detail.html")
        self.assertEqual(response.context["cook"], self.cook_1)

    def test_cook_create_view(self):
        response = self.client.post(self.create_url, self.cook_data)
        self.assertEqual(Cook.objects.count(), 4)
        self.assertRedirects(response, self.list_url)

    def test_cook_update_view(self):
        update_data = {"years_of_experience": 6}
        response = self.client.post(self.update_url, update_data)
        self.cook_1.refresh_from_db()
        self.assertEqual(self.cook_1.years_of_experience, 6)
        self.assertRedirects(response, self.list_url)

    def test_cook_delete_view(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(Cook.objects.count(), 2)
        self.assertRedirects(response, self.list_url)

    def test_search_filter_by_username(self):
        response = self.client.get(self.list_url, {"username": "cook1"})
        self.assertEqual(len(response.context["cook_list"]), 1)
        self.assertEqual(response.context["cook_list"][0], self.cook_1)
