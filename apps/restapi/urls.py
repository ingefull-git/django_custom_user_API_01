from django.urls import path

from apps.restapi import views

app_name = 'restapi'


urlpatterns = [
    path('', views.user_list_api_view, name="api-user-list"),
    path('register', views.user_register_api_view, name="api-user-register"),
    path('<int:pk>/update', views.user_get_update_api_view, name="api-user-get-put"),
]