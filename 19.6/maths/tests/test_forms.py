from django.test import TestCase

from maths.forms import ResultForm
from maths.models import Result


class ResultFormTest(TestCase):
    def test_result_save_correct_data(self):
        data = {"value": 200}
        self.assertEqual(len(Result.objects.all()), 0)
        form = ResultForm(data=data)
        self.assertTrue(form.is_valid())
        r = form.save()
        self.assertIsInstance(r, Result)
        self.assertEqual(r.value, 200)
        self.assertIsNotNone(r.id)
        self.assertIsNone(r.error)

    def test_result_rejects_both_value_and_error(self):
        data = {"value": 200, "error": "boom"}
        form = ResultForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Podaj tylko jedną z wartości", form.errors["__all__"])

    def test_result_rejects_empty_data(self):
        form = ResultForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("Nie podano żadnej wartości!", form.errors["__all__"])
