from rest_framework import routers

from books import api_views as books_views

router = routers.DefaultRouter()
router.register("books", books_views.BookViewSet)
router.register("authors", books_views.AuthorViewSet)
router.register("tags", books_views.TagViewSet)
