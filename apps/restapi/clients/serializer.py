from rest_framework import serializers
from apps.clients.models import Client

class ClientsSerializer(serializers.Serializer):

    class Meta:
        model = Client
        fields = "__all__"