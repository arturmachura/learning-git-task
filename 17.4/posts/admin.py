from django.contrib import admin

from .models import Author, Post


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("email", "bio")
    search_fields = ("email",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created", "modified")
    search_fields = ("title", "content")
    list_filter = ("author", "created")
