from django.urls import path, include

from apps.restapi.clients import views


urlpatterns = [
    # path('list', views.client_list_api_view),
    path('list', views.ClientListApiView.as_view()),
    path('list-create', views.client_list_create_view),
    path('generic-list-create', views.ClientListCreateApiView.as_view()),
    # path('<int:pk>/update', views.ClientRetrieveUpdateApiView.as_view()),
    path('<int:pk>/update', views.client_retieve_update_api_view),
    path('<int:pk>/detail', views.client_retrieve_update_delete_view),
]