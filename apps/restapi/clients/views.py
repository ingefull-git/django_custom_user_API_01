from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ...clients.models import Client
from .pagination import CustomLimitPagination, CustomPageNumberPagination

from .serializer import ClientsSerializer


# @api_view(['GET',])
# # @permission_classes([IsAuthenticated,])
# def client_list_api_view(request):
#     clients = Client.objects.all()
#     serializer = ClientsSerializer(clients, many=True)
#     return Response(serializer.data)

class ClientListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    authentication_classes = [TokenAuthentication,]
    queryset = Client.objects.all().order_by('-created')
    serializer_class = ClientsSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'fname', 'lname', 'email', 'created', 'updated']


@api_view(['GET', 'PUT',])
def client_get_update_api_view(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ClientsSerializer(client)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ClientsSerializer(client, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data = {
                'response': 'client updated successfully',
                'id': client.id,
                'fname': client.fname,
                'lname': client.lname,
                'email': client.email,
                'created': client.created,
                'updated': client.updated
            }
            return Response(data=data)
        data = {'response': 'error: verify data'}
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientRetrieveUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = Client.objects.all().order_by('-created')
    serializer_class = ClientsSerializer

