from django.urls import path

from apps.restapi.customuser import views


urlpatterns = [
    path('list', views.user_list_api_view),
    path('register', views.user_register_api_view),
    path('login', views.user_login_api_view),
    path('<int:pk>/update', views.user_get_update_api_view),
]