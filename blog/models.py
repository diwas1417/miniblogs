"""
models.py
Defines database models for users and posts in the application.
"""

from django.db import models


class Post(models.Model):
    """Model representing a blog post."""

    title = models.CharField(max_length=100)
    desc = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the title of the post."""
        return self.title
