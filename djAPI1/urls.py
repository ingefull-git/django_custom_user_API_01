from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('apps.restapi.urls', namespace="restapi")),
    path('', include('apps.clients.urls', namespace="clients")),
]
