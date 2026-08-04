from django.contrib import admin

from .models import Author, Book, Borrow, Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("word",)
    search_fields = ("word",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "pages")
    list_filter = ("author", "tags")
    search_fields = ("title", "description")


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "borrowed_at", "is_returned", "returned_at")
    list_filter = ("is_returned",)
    search_fields = ("book__title", "user__username")
