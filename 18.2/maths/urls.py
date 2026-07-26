from django.urls import path

from maths.views import add, div, histories, math, math_details, mul, results_list, sub

app_name = "maths"

urlpatterns = [
    path("", math, name="math"),
    path("add/<int:a>/<int:b>", add, name="add"),
    path("sub/<int:a>/<int:b>", sub, name="sub"),
    path("mul/<int:a>/<int:b>", mul, name="mul"),
    path("div/<int:a>/<int:b>", div, name="div"),
    path("histories/", histories, name="histories"),
    path("histories/<int:pk>", math_details, name="math_details"),
    path("results/", results_list, name="results"),
]
