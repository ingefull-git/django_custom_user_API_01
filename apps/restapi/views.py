from django.shortcuts import render

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from apps.customuser.models import CustomUser
from apps.restapi.serializers import CustomUserRegisterSerializer

@api_view(['GET',])
@permission_classes([IsAuthenticatedOrReadOnly],)
def user_list_api_view(request):
    users = CustomUser.objects.all()
    serializer = CustomUserRegisterSerializer(users, many=True)
    return Response(serializer.data)

