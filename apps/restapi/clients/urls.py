from django.urls import path, include

from apps.restapi.clients import views

app_name = 'clients-api'


urlpatterns = [
    path('list', views.client_list_api_view, name='client-api-list'),
]