from django.urls import path

from .views import hello_world, hello_name

app_name = "greetings"

urlpatterns = [
    path('', hello_world, name="hello_world"),
    path('<str:name>', hello_name, name="hello_name"),
]
