from django import forms

from .models import Author, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "author"]


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["email", "bio"]
