from django.urls import path, include

from apps.restapi.clients import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('list-clients', views.ClientViewset, basename='clients-viewset')
router.register('generic-clients', views.ClientGenericViewset, basename='clients-generic-viewset')
router.register('model-clients', views.ClientModelViewset, basename='clients-model-viewset')


urlpatterns = [
    # path('list', views.client_list_api_view),
    path('list', views.ClienGenericsListApiView.as_view()),
    path('list-create', views.client_list_create_view),
    path('generic-list-create', views.ClientListCreateApiView.as_view()),
    # path('<int:pk>/update', views.ClientRetrieveUpdateApiView.as_view()),
    path('<int:pk>/update', views.client_retieve_update_api_view),
    path('<int:pk>/detail', views.client_retrieve_update_delete_view),
    path('viewset/', include(router.urls)),
]