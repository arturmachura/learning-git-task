from django.test import Client, TestCase

from maths.models import Math, Result


class MathViewsTest(TestCase):
    def setUp(self):
        Math.objects.create(operation="sub", a=20, b=30)
        self.client = Client()

    def test_maths_histories(self):
        response = self.client.get("/maths/histories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["maths"]), 1)

    def test_add_creates_math_and_result(self):
        response = self.client.get("/maths/add/1/2")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wynik operacji 1 + 2 wynosi 3", response.content)
        self.assertTrue(Math.objects.filter(operation="add", a=1, b=2).exists())
        self.assertTrue(Result.objects.filter(value=3).exists())

    def test_div_by_zero_adds_error_message(self):
        response = self.client.get("/maths/div/1/0", follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertTrue(any("Dzielenie przez zero" in str(m) for m in messages))


class MathViewsPaginationTest(TestCase):
    fixtures = ["math", "result"]

    def setUp(self):
        self.client = Client()

    def test_get_first_page_has_5_entries(self):
        response = self.client.get("/maths/histories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["maths"]), 5)

    def test_get_last_page(self):
        response = self.client.get("/maths/histories/?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["maths"].number, 3)
        self.assertFalse(response.context["maths"].has_next())

    def test_filter_by_operation(self):
        response = self.client.get("/maths/histories/?operation=add")
        self.assertEqual(response.status_code, 200)
        for entry in response.context["maths"]:
            self.assertEqual(entry.operation, "add")


class ResultsListViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_results_list(self):
        response = self.client.get("/maths/results/")
        self.assertEqual(response.status_code, 200)

    def test_post_creates_result(self):
        response = self.client.post("/maths/results/", data={"value": 42}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Result.objects.filter(value=42).exists())
