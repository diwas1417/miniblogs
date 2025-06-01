"""
test_views.py
Unit tests for views in the blog app.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class BasicViewTests(TestCase):
    """Test suite for basic view functionality."""

    def setUp(self):
        """Set up test environment."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_home_page_status_code(self):
        """Test if home page returns status 200."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        """Test if dashboard redirects for unauthenticated users."""
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, "/login/?next=/dashboard/")

    def test_login_with_valid_credentials(self):
        """Test login functionality with valid credentials."""
        login = self.client.login(username="testuser", password="testpass")
        self.assertTrue(login)
