from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from dingo.api import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/v1/', include(router.urls)),
    path('', include('greetings.urls')),
    path('maths/', include('maths.urls')),
    path('posts/', include('posts.urls')),
    path('books/', include('books.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
