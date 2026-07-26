from unittest import TestCase

from django.urls import resolve
from django.urls.exceptions import Resolver404

from posts.views import author_details, authors_list, post_details, posts_list


class TestPostsUrls(TestCase):
    def test_resolution_for_posts_list(self):
        resolver = resolve("/posts/")
        self.assertEqual(resolver.func, posts_list)

    def test_resolution_for_post_details(self):
        resolver = resolve("/posts/1/")
        self.assertEqual(resolver.func, post_details)

    def test_resolution_for_authors_list(self):
        resolver = resolve("/posts/authors/")
        self.assertEqual(resolver.func, authors_list)

    def test_resolution_for_author_details(self):
        resolver = resolve("/posts/authors/1/")
        self.assertEqual(resolver.func, author_details)

    def test_non_integer_pk_is_404(self):
        with self.assertRaises(Resolver404):
            resolve("/posts/abc/")
