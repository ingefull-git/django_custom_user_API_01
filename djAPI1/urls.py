import debug_toolbar

from django.contrib import admin
from django.urls import path, include

from rest_framework.schemas import SchemaGenerator, get_schema_view
from rest_framework.documentation import include_docs_urls
# from rest_framework.renderers import JSONOpenAPIRenderer, CoreJSONRenderer

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Django CustomUser RestAPI",
      default_version='v1',
      description="Django CustomUser RestApi",
      terms_of_service="#",
      contact=openapi.Contact(email="rsosa.ingefull@gmail.com"),
      license=openapi.License(name="#"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('apps.restapi.urls', namespace="restapi")),
    path('', include('apps.clients.urls', namespace="clients")),
    path('authuser/', include('apps.authuser.urls', namespace='authuser')),
    path('accounts/', include('allauth.urls')),
    # path('docs/', include_docs_urls(title='RestAPI')),
    # path('schema', get_schema_view(
    #     title="Django RestAPI",
    #     description="API Schema …",
    #     version="1.0.0",
        
    # ), name='openapi-schema'),
    path('docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('__debug__/', include(debug_toolbar.urls)),
]
