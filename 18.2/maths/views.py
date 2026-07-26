from django.contrib import messages
from django.shortcuts import get_object_or_404, render

from maths.forms import ResultForm
from maths.models import Math, Result


def math(request):
    return render(request, "maths/main.html", {"title": "maths"})


def add(request, a, b):
    wynik = a + b
    result = Result.objects.get_or_create(value=wynik)[0]
    Math.objects.create(operation="add", a=a, b=b, result=result)
    c = {"a": a, "b": b, "operacja": "+", "wynik": wynik, "title": "dodawanie"}
    return render(request, "maths/operation.html", c)


def sub(request, a, b):
    wynik = a - b
    result = Result.objects.get_or_create(value=wynik)[0]
    Math.objects.create(operation="sub", a=a, b=b, result=result)
    c = {"a": a, "b": b, "operacja": "-", "wynik": wynik, "title": "odejmowanie"}
    return render(request, "maths/operation.html", c)


def mul(request, a, b):
    wynik = a * b
    result = Result.objects.get_or_create(value=wynik)[0]
    Math.objects.create(operation="mul", a=a, b=b, result=result)
    c = {"a": a, "b": b, "operacja": "*", "wynik": wynik, "title": "mnożenie"}
    return render(request, "maths/operation.html", c)


def div(request, a, b):
    if b == 0:
        wynik = "Error"
        result = Result.objects.get_or_create(error="ZeroDivisionError")[0]
        messages.add_message(request, messages.ERROR, "Dzielenie przez zero!")
    else:
        wynik = a / b
        result = Result.objects.get_or_create(value=wynik)[0]
    Math.objects.create(operation="div", a=a, b=b, result=result)
    c = {"a": a, "b": b, "operacja": "/", "wynik": wynik, "title": "dzielenie"}
    return render(request, "maths/operation.html", c)


def histories(request):
    maths = Math.objects.all()
    return render(request, "maths/histories.html", {"maths": maths, "title": "histories"})


def math_details(request, pk):
    entry = get_object_or_404(Math, pk=pk)
    return render(request, "maths/math_details.html", {"math": entry, "title": "math details"})


def results_list(request):
    if request.method == "POST":
        form = ResultForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Utworzono nowy Result!!")
        else:
            for error in form.non_field_errors():
                messages.add_message(request, messages.ERROR, error)
    else:
        form = ResultForm()

    results = Result.objects.all()
    return render(
        request,
        "maths/results.html",
        {"results": results, "form": form, "title": "results"},
    )
