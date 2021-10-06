from rest_framework import serializers

from rest_framework.exceptions import ValidationError
from apps.customuser.models import CustomUser


class CustomUserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'created', 'login', 'password', 'password2')


    def save(self, *args, **kwargs):
        user = CustomUser(
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

