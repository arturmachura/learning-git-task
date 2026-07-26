from unittest import TestCase

from django.urls import resolve

from greetings.views import hello_name, hello_world


class TestGreetingsUrls(TestCase):
    def test_resolution_for_hello_world(self):
        resolver = resolve("/greetings/")
        self.assertEqual(resolver.func, hello_world)

    def test_resolution_for_hello_name(self):
        resolver = resolve("/greetings/rafal")
        self.assertEqual(resolver.func, hello_name)
