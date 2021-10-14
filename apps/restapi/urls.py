from django.urls import path, include


app_name = 'restapi'


urlpatterns = [
    path('user/', include('apps.restapi.customuser.urls')),
    path('client/', include('apps.restapi.clients.urls')),

]