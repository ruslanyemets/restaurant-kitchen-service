from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("kitchen.urls", namespace="kitchen")),
        path("accounts/", include("django.contrib.auth.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + debug_toolbar_urls()
)
