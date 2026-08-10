from django.shortcuts import render


def welcome(request):
    return render(request, "greetings/welcome.html", {"title": "Welcome"})


def about(request):
    return render(request, "greetings/about.html", {"title": "About"})


def contact(request):
    return render(request, "greetings/contact.html", {"title": "Contact"})
