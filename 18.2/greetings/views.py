from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.html import escape


def hello_world(request):
    return HttpResponse("Hello World!")


def hello_name(request, name):
    if not name.isalpha():
        return HttpResponseBadRequest("Name must contain only letters.")
    return HttpResponse(f"Hello {escape(name.capitalize())}!")
