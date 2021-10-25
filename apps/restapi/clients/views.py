from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework.parsers import JSONParser
from rest_framework import generics, status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets

from ...clients.models import Client
from .pagination import CustomLimitPagination, CustomPageNumberPagination
from .serializer import ClientSerializer

@api_view(['GET', 'POST'])
@permission_classes([AllowAny,])
# @csrf_exempt
def client_list_create_view(request):
    """
    List all the clients or create a new client.
    """
    if request.method == 'POST':

        # data = JSONParser().parse(request)
        data = request.data
        serializer = ClientsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data, status=201)
            return Response(serializer.data)
        # return JsonResponse(serializer.errors, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    clients = Client.objects.all()

    serializer = ClientsSerializer(clients, many=True)
    # return JsonResponse(serializer.data, safe=False)
    return Response(serializer.data)



@api_view(['GET',])
# @permission_classes([IsAuthenticated,])
def client_list_api_view(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


class ClientListCreateApiView(generics.GenericAPIView, 
                                mixins.ListModelMixin, 
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin
                                ):
    queryset = Client.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = ClientsSerializer
    lookup_field = "id"

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)
    
    def delete(self, request, id=None):
        return self.destroy(request, id)


class ClientListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    authentication_classes = [TokenAuthentication,]
    queryset = Client.objects.all().order_by('-created')
    serializer_class = ClientSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'fname', 'lname', 'email', 'created', 'updated']


class ClientViewset(viewsets.ViewSet):
    def list(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        # clients = Client.objects.all()
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            request.data['response'] = "updated successfully"
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientGenericViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ClientModelViewset(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


@api_view(['GET', 'PUT',])
def client_retieve_update_api_view(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ClientSerializer(client, data=request.data)
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
    serializer_class = ClientSerializer


@api_view(['GET', 'PUT', 'DELETE'])
# @csrf_exempt
def client_retrieve_update_delete_view(request, pk):
    """
    Can retrieve, update and delete client.
    """
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ClientSerializer(client, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        client.delete()
        return HttpResponse(status=204)