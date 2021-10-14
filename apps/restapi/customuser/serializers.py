from rest_framework import serializers

from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'created', 'login', 'password', 'password2')


    def save(self, *args, **kwargs):
        try:
            userid = self.data['id']
        except:
            userid = None
        if not userid:
            user = User(
                email = self._validated_data['email'],
                username = self.validated_data['username'],
            )
            password = self.validated_data['password']
            password2 = self.validated_data['password2']
            if password != password2:
                raise ValidationError({'password':'Password must match..!!'})
            user.set_password(password)
            user.save()
            return user
        else:
            try:
                user = User.objects.get(pk=userid)
            except User.DoesNotExist:
                user = None
            user.email=self.validated_data['email']
            user.username=self.validated_data['username']
            password = self.validated_data['password']
            user.set_password(password)
            user.save()
            return user


class CustomUserLoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

