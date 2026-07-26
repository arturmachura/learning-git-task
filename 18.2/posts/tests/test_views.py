from django.test import Client, TestCase

from posts.models import Author, Post


class PostsListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(email="eve@example.com")
        Post.objects.create(title="Hello", content="World", author=self.author)

    def test_get_posts_list(self):
        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 1)
        self.assertIn(b"Hello", response.content)

    def test_post_creates_new_post(self):
        response = self.client.post(
            "/posts/",
            data={"title": "New post", "content": "New content", "author": self.author.pk},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(title="New post").exists())


class PostDetailsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(email="frank@example.com")
        self.post = Post.objects.create(title="Details post", content="Text", author=self.author)

    def test_post_details_returns_200(self):
        response = self.client.get(f"/posts/{self.post.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["post"], self.post)

    def test_post_details_404_for_missing_post(self):
        response = self.client.get("/posts/9999/")
        self.assertEqual(response.status_code, 404)


class AuthorsListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Author.objects.create(email="gina@example.com")

    def test_get_authors_list(self):
        response = self.client.get("/posts/authors/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["authors"]), 1)

    def test_post_creates_new_author(self):
        response = self.client.post(
            "/posts/authors/", data={"email": "harry@example.com"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Author.objects.filter(email="harry@example.com").exists())


class AuthorDetailsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(email="ivan@example.com")

    def test_author_details_returns_200(self):
        response = self.client.get(f"/posts/authors/{self.author.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["author"], self.author)

    def test_author_details_404_for_missing_author(self):
        response = self.client.get("/posts/authors/9999/")
        self.assertEqual(response.status_code, 404)
