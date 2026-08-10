from django.test import Client, TestCase


class GreetingsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_welcome_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_about_returns_200(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_contact_returns_200(self):
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)
