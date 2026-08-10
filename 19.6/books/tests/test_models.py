from django.contrib.auth import get_user_model
from django.test import TestCase

from books.models import Author, Book, Borrow

User = get_user_model()


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Jane Doe")
        self.book = Book.objects.create(title="Some Book", author=self.author)
        self.user = User.objects.create_user(username="alice", password="secret123")

    def test_book_is_on_shelf_by_default(self):
        self.assertTrue(self.book.is_on_shelf())

    def test_book_not_on_shelf_when_borrowed(self):
        Borrow.objects.create(book=self.book, user=self.user)
        self.assertFalse(self.book.is_on_shelf())

    def test_book_back_on_shelf_after_return(self):
        borrow = Borrow.objects.create(book=self.book, user=self.user)
        borrow.is_returned = True
        borrow.save()
        self.assertTrue(self.book.is_on_shelf())

    def test_book_str(self):
        self.assertEqual(str(self.book), "Some Book (Jane Doe)")
