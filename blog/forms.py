"""
Forms module to handle user registration, login, and blog post forms.
"""

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from django.utils.translation import gettext_lazy as _

from .models import Post


class signupform(UserCreationForm):
    """Form for user registration using Django's UserCreationForm."""

    password1 = forms.CharField(
        label="Password", widget=PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password", widget=PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        error_messages = {"username": {"required": "Enter your name"}}


class loginform(AuthenticationForm):
    """Form for user login extending Django's AuthenticationForm."""

    username = UsernameField(
        widget=forms.Textarea(attrs={"autofocus": True, "class": "form-control"})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts."""

    class Meta:
        model = Post
        fields = ["title", "desc"]
        labels = {"title": "Title", "desc": "Description"}
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "desc": forms.Textarea(attrs={"class": "form-control"}),
        }
