from rest_framework import serializers
from apps.clients.models import Client

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"
    
    def update(self, validated_data):
        fnameval = validated_data('fname').pop()
        print(validated_data)

