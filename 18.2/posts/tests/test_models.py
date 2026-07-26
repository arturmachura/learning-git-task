from django.test import TestCase

from posts.models import Author, Post


class AuthorModelTest(TestCase):
    def setUp(self):
        Author.objects.create(email="alice@example.com", bio="Bio text")

    def test_author_str(self):
        author = Author.objects.get(email="alice@example.com")
        self.assertEqual(str(author), "alice@example.com")


class PostModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(email="bob@example.com")
        Post.objects.create(title="First post", content="Some content", author=self.author)

    def test_post_str(self):
        post = Post.objects.get(title="First post")
        self.assertEqual(str(post), "First post (by bob@example.com)")

    def test_post_created_and_modified_are_set(self):
        post = Post.objects.get(title="First post")
        self.assertIsNotNone(post.created)
        self.assertIsNotNone(post.modified)

    def test_post_modified_updates_on_save(self):
        post = Post.objects.get(title="First post")
        first_modified = post.modified
        post.title = "Updated title"
        post.save()
        post.refresh_from_db()
        self.assertGreaterEqual(post.modified, first_modified)
