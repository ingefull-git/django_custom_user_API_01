from django.urls import path, include
from apps.clients import views

app_name = 'clients'

urlpatterns = [
    path('', views.clients_list_view, name="client-list"),
]