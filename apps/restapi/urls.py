from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



app_name = 'restapi'


urlpatterns = [
    path('user/', include('apps.restapi.customuser.urls')),
    path('client/', include('apps.restapi.clients.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]