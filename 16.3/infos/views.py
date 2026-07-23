from django.shortcuts import render


def home(request):
    return render(request, "infos/home.html", {"active": "home"})


def me(request):
    return render(request, "infos/me.html", {"active": "me"})


def contact(request):
    return render(request, "infos/contact.html", {"active": "contact"})
