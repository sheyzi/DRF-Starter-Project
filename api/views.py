from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from cfehome.serializers import MessageSerializer


class HealthCheckView(generics.GenericAPIView):
    api_tags = ["Health Check"]
    api_operation_id = "health_check"
    api_summary = "Health Check"
    api_description = "Check if the API is running"
    filter_backends = []

    serializer_class = MessageSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: MessageSerializer,
        },
    )
    def get(request):
        return Response(MessageSerializer({"message": "OK"}).data)


schema_view = get_schema_view(
    openapi.Info(
        title="Spek & Boonen ERP API",
        default_version="v1",
        description="""
        This is the API documentation for the Spek & Boonen ERP API.

        Filter, search and order fields are available for all endpoints that return a list of objects.

        To filter, search or order, append the following query parameters to the endpoint URL:
        - `?field_name=<value>` to filter by a specific field
        - `?search=<search_term>` to search for a specific term
        - `?ordering=<field_name>` to order by a specific field
        """,
        contact=openapi.Contact(email="oluwaseyifunmi@mafflle.com.ng"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(SessionAuthentication,),
)
