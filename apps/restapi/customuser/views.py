from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from apps.customuser.models import CustomUser
from apps.restapi.customuser.serializers import CustomUserSerializer, CustomUserLoginSerializer


@api_view(['POST',])
@permission_classes([AllowAny])
def user_register_api_view(request):
    data = {}
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'response': "new user registered successfully",
                'email': user.email,
                'username': user.username
            }
        else:
            data = serializer.errors
        return Response(data)


@api_view(['POST',])
@permission_classes([AllowAny])
def user_login_api_view(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            context['response'] = "invalid user..!!"
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserLoginSerializer(user, data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                try:
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
                context = {
                    'response': "successfully authenticated",
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'token': token.key
                }
            else:
                context = {
                    'response': "error authenticating",
                    'error_message': "invalid credentials"
                }
            return Response(context)
    context = {
        'response': "invalid serializer..!!",
        'errors': serializer.errors,
    }
    return Response(context)


@api_view(['GET',])
@permission_classes([IsAuthenticatedOrReadOnly],)
def user_list_api_view(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT',])
@permission_classes([IsAuthenticated,])
def user_get_update_api_view(request, pk):
    data = {}
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'response': "user updated successfully..!!",
                'email': user.email,
                'username': user.username,
                'password': user.password,
                'login': user.login
            }
            return Response(data)
        data = {'response':"Verify the content..!!"}
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


