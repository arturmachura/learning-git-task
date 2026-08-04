from django.urls import path

from .views import author_details, authors_list, book_details, books_list, my_borrows

app_name = "books"

urlpatterns = [
    path("", books_list, name="books_list"),
    path("borrows/", my_borrows, name="my_borrows"),
    path("authors/", authors_list, name="authors_list"),
    path("authors/<int:pk>/", author_details, name="author_details"),
    path("<int:pk>/", book_details, name="book_details"),
]
