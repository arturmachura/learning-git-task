from django.urls import path

from .views import home, me, contact

urlpatterns = [
    path('', home, name='home'),
    path('me', me, name='me'),
    path('contact', contact, name='contact'),
]
