from django.conf import settings
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    word = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["word"]

    def __str__(self):
        return self.word


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    description = models.TextField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    cover = models.ImageField(upload_to="covers/%Y/%m/%d", null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="books", blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.author})"

    def is_on_shelf(self):
        return not self.borrows.filter(is_returned=False).exists()


class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrows"
    )
    borrowed_at = models.DateTimeField(auto_now_add=True)
    is_returned = models.BooleanField(default=False)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-borrowed_at"]

    def __str__(self):
        status = "returned" if self.is_returned else "borrowed"
        return f"{self.book} by {self.user} ({status})"
