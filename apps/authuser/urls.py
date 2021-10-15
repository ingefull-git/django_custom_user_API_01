from django.urls import path
from . import views

app_name = 'authuser'


urlpatterns = [
    path('login/', views.loginview, name='login-view'),
    path('logout/', views.logoutview, name='logout-view'),
]
