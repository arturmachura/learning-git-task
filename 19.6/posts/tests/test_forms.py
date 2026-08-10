from django.test import TestCase

from posts.forms import AuthorForm, PostForm
from posts.models import Author, Post


class AuthorFormTest(TestCase):
    def test_author_form_saves_valid_data(self):
        form = AuthorForm(data={"email": "carol@example.com", "bio": "Hi there"})
        self.assertTrue(form.is_valid())
        author = form.save()
        self.assertIsInstance(author, Author)
        self.assertEqual(author.email, "carol@example.com")

    def test_author_form_requires_email(self):
        form = AuthorForm(data={"bio": "Missing email"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class PostFormTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(email="dave@example.com")

    def test_post_form_saves_valid_data(self):
        form = PostForm(
            data={"title": "A title", "content": "Content", "author": self.author.pk}
        )
        self.assertTrue(form.is_valid())
        post = form.save()
        self.assertIsInstance(post, Post)
        self.assertEqual(post.author, self.author)

    def test_post_form_requires_author(self):
        form = PostForm(data={"title": "A title", "content": "Content"})
        self.assertFalse(form.is_valid())
        self.assertIn("author", form.errors)
