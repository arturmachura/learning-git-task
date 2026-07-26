from django.test import Client, TestCase


class GreetingsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_hello_world(self):
        response = self.client.get("/greetings/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello World!")

    def test_hello_name_capitalizes(self):
        response = self.client.get("/greetings/rafal")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello Rafal!")

    def test_hello_name_rejects_digits(self):
        response = self.client.get("/greetings/123")
        self.assertEqual(response.status_code, 400)

    def test_hello_name_escapes_html(self):
        response = self.client.get("/greetings/%3Cscript%3E")
        self.assertEqual(response.status_code, 400)
