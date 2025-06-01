"""
models.py
Defines database models for users and posts in the application.
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    """Model representing a blog post."""

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    desc = models.TextField()
