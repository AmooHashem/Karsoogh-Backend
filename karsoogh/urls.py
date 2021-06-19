from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from karsoogh import settings

urlpatterns = \
    [
        path('admin/', admin.site.urls),
        path('account/', include('Account.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
