from django.urls import path

from . import views

urlpatterns = [
    path("", views.HealthCheckView.as_view(), name="health_check"),
    path(
        "swagger/",
        views.schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger_schema",
    ),
    path(
        "redoc/",
        views.schema_view.with_ui("redoc", cache_timeout=0),
        name="swagger_schema",
    ),
]
