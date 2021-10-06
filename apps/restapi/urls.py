from django.urls import path

from apps.restapi import views

app_name = 'restapi'


urlpatterns = [
    path('', views.user_list_api_view, name="api-list"),
]