from rest_framework import serializers
from apps.clients.models import Client

class ClientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"