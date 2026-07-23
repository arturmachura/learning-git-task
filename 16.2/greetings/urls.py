from django.urls import path

from .views import hello_world, hello_name

urlpatterns = [
    path('', hello_world),
    path('<str:name>', hello_name),
]
