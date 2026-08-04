from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from books.models import Author, Book, Borrow

User = get_user_model()


class BooksListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        author = Author.objects.create(name="Jane Doe")
        Book.objects.create(title="Some Book", author=author)

    def test_books_list_returns_200(self):
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["books"]), 1)


class BookDetailsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="Jane Doe")
        self.book = Book.objects.create(title="Some Book", author=self.author)
        self.user = User.objects.create_user(username="alice", password="secret123")

    def test_book_details_returns_200(self):
        response = self.client.get(f"/books/{self.book.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_borrowing_requires_login(self):
        response = self.client.post(f"/books/{self.book.pk}/")
        self.assertRedirects(response, "/accounts/login/")
        self.assertFalse(Borrow.objects.exists())

    def test_logged_in_user_can_borrow_available_book(self):
        self.client.login(username="alice", password="secret123")
        response = self.client.post(f"/books/{self.book.pk}/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Borrow.objects.filter(book=self.book, user=self.user).exists())

    def test_cannot_borrow_a_book_already_borrowed(self):
        Borrow.objects.create(book=self.book, user=self.user)
        other_user = User.objects.create_user(username="bob", password="secret123")
        self.client.login(username="bob", password="secret123")
        self.client.post(f"/books/{self.book.pk}/", follow=True)
        self.assertEqual(Borrow.objects.filter(book=self.book).count(), 1)


class AuthorsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="Jane Doe")
        Book.objects.create(title="Some Book", author=self.author)

    def test_authors_list_returns_200(self):
        response = self.client.get("/books/authors/")
        self.assertEqual(response.status_code, 200)

    def test_author_details_shows_books(self):
        response = self.client.get(f"/books/authors/{self.author.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Some Book", response.content)


class MyBorrowsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        author = Author.objects.create(name="Jane Doe")
        self.book = Book.objects.create(title="Some Book", author=author)
        self.user = User.objects.create_user(username="alice", password="secret123")
        self.borrow = Borrow.objects.create(book=self.book, user=self.user)

    def test_my_borrows_requires_login(self):
        response = self.client.get("/books/borrows/")
        self.assertEqual(response.status_code, 302)

    def test_my_borrows_lists_own_borrows(self):
        self.client.login(username="alice", password="secret123")
        response = self.client.get("/books/borrows/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["borrows"]), 1)

    def test_returning_a_book(self):
        self.client.login(username="alice", password="secret123")
        response = self.client.post(
            "/books/borrows/", data={"borrow_id": self.borrow.id}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.borrow.refresh_from_db()
        self.assertTrue(self.borrow.is_returned)
        self.assertIsNotNone(self.borrow.returned_at)
