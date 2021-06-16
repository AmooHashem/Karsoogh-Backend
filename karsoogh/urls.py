from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from karsoogh import settings

urlpatterns = \
    [
        path('admin/', admin.site.urls),
        path('formula0/', include('Formula0.urls')),
        path('account/', include('Account.urls')),
        path('exam/', include('Exam.urls')),
        path('event/', include('Event.urls')),
        path('', include('Api.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
