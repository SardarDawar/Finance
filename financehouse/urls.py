from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # django admin urls
    path('admin/', admin.site.urls),

    # my app urls
    path('', include('common.urls')),
    path('', include('users.urls')),
    path('projects/', include('projects.urls')),
    path('blogs/', include('blogs.urls')),
    path('news/', include('news.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)