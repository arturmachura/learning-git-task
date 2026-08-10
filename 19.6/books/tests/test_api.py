from django.test import TestCase

from books.models import Author, Book


class BooksApiTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Jane Doe")
        self.book = Book.objects.create(title="Some Book", author=self.author)

    def test_list_books(self):
        response = self.client.get("/api/v1/books/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_retrieve_book(self):
        response = self.client.get(f"/api/v1/books/{self.book.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Some Book")

    def test_create_book(self):
        response = self.client.post(
            "/api/v1/books/",
            data={"title": "New Book", "author": self.author.pk},
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_delete_book(self):
        response = self.client.delete(f"/api/v1/books/{self.book.pk}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())


class AuthorsApiTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Jane Doe")

    def test_list_authors(self):
        response = self.client.get("/api/v1/authors/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_author(self):
        response = self.client.post("/api/v1/authors/", data={"name": "New Author"})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Author.objects.filter(name="New Author").exists())
