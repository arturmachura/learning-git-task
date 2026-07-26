from unittest import TestCase

from django.urls import resolve

from greetings.views import about, contact, welcome


class TestGreetingsUrls(TestCase):
    def test_resolution_for_welcome(self):
        resolver = resolve("/")
        self.assertEqual(resolver.func, welcome)

    def test_resolution_for_about(self):
        resolver = resolve("/about/")
        self.assertEqual(resolver.func, about)

    def test_resolution_for_contact(self):
        resolver = resolve("/contact/")
        self.assertEqual(resolver.func, contact)
