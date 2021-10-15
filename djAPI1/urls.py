from django.contrib import admin
from django.urls import path, include

from rest_framework.schemas import SchemaGenerator, get_schema_view
from rest_framework.documentation import include_docs_urls
# from rest_framework.renderers import JSONOpenAPIRenderer, CoreJSONRenderer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('apps.restapi.urls', namespace="restapi")),
    path('', include('apps.clients.urls', namespace="clients")),
    path('docs/', include_docs_urls(title='RestAPI')),
    path('schema', get_schema_view(
        title="Django RestAPI",
        description="API Schema …",
        version="1.0.0",
        
    ), name='openapi-schema'),
]
