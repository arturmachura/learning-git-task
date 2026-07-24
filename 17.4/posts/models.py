from django.db import models


class Author(models.Model):
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    def __str__(self):
        return f"{self.title} (by {self.author.email})"
