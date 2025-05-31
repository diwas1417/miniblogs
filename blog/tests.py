from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class BasicTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_home_page_status_code(self):
        response = self.client.get(
            reverse("home")
        )  # adjust if your URL name is different
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, "/login/?next=/dashboard/")

    def test_login_with_valid_credentials(self):
        login = self.client.login(username="testuser", password="testpass")
        self.assertTrue(login)
