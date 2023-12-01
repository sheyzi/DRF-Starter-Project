from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path(
        "api/auth/",
        include(
            "accounts.urls",
            namespace="accounts",
        ),
    ),
    path("api/inventory/", include("inventory.urls")),
]
