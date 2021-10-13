from django.urls import path, include

from apps.restapi.customuser import views

app_name = 'restapi'


urlpatterns = [
    path('user/', include('apps.restapi.customuser.urls')),
]