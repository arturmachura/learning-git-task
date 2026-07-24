from django.urls import path

from .views import author_details, authors_list, post_details, posts_list

app_name = "posts"

urlpatterns = [
    path("", posts_list, name="posts_list"),
    path("<int:pk>/", post_details, name="post_details"),
    path("authors/", authors_list, name="authors_list"),
    path("authors/<int:pk>/", author_details, name="author_details"),
]
