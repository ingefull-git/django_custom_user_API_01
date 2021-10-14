from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.clients.models import Client

from apps.restapi.clients.serializer import ClientsSerializer


@api_view(['GET',])
@permission_classes([IsAuthenticatedOrReadOnly,])
def client_list_api_view(request):
    clients = Client.objects.all()
    serializer = ClientsSerializer(clients, many=True)
    return Response(serializer.data)
