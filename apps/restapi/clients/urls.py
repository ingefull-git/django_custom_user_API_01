from django.urls import path, include

from apps.restapi.clients import views


urlpatterns = [
    # path('list', views.client_list_api_view),
    path('list', views.ClientListApiView.as_view()),
    # path('<int:pk>/update', views.ClientRetrieveUpdateApiView.as_view()),
    path('<int:pk>/update', views.client_get_update_api_view),
]