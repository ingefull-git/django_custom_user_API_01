from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

from rest_framework.parsers import JSONParser
from rest_framework import generics, status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

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
        serializer = ClientSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data, status=201)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    clients = Client.objects.all()

    serializer = ClientSerializer(clients, many=True)
    # return JsonResponse(serializer.data, safe=False)
    return Response(serializer.data)



@api_view(['GET',])
# @permission_classes([IsAuthenticated,])
def client_list_api_view(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


class ClientAPIView(APIView):
    pagination_class = PageNumberPagination

    def get_object(self, pk):
        try:
            # client = Client.objects.get(pk=pk)
            client = get_object_or_404(Client, pk=pk)
            return client
        except Client.DoesNotExist:
            return Response(status = status.HTTP_304_NOT_MODIFIED)

    def get(self, request, pk=None):
        if pk:
            query = self.get_object(pk)
            serializer = ClientSerializer(query)
            return Response(serializer.data)
        else:
            query = Client.objects.all()
            status = request.query_params.get('status')
            if status:
                query = Client.objects.filter(status=status)
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(query, request)
            serializer = ClientSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientMixinsApiView(generics.GenericAPIView, 
                                mixins.ListModelMixin, 
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin
                                ):
    queryset = Client.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = ClientSerializer
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


class ClientGenericsListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    authentication_classes = [TokenAuthentication,]
    # queryset = Client.objects.all().order_by('-created')
    serializer_class = ClientSerializer
    # pagination_class = CustomPageNumberPagination
    # filter_backends = [SearchFilter, OrderingFilter]
    # search_fields = ['id', 'fname', 'lname', 'email', 'created', 'updated']
    # search_fields = ['lname']
    # lookup_field = "status"

    def get_queryset(self, request):
        clients = Client.objects.all()
        status = request.query_params.get('status')
        if status:
            clients= Client.objects.filter(status=status).order_by('-created')
            print("Status: ", status)
        return clients



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


class ClientCustomAPIView(APIView):
    ''' add comment to the endpoint for swagger'''
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, created):
        # clients = Client.objects.filter(created__date=created).values('status').distinct()
        # clients = Client.objects.filter(created__date=created).annotate(Count('status', distinct=True)).distinct().order_by('status')
        result = []
        statuses = Client.objects.values('pk').filter(created__date=created).values_list('status', flat=True).distinct()
        clients = Client.objects.values('pk').filter(created__date=created).values('status')
        # clients = Client.objects.raw('SELECT DISTINCT ("clients_client"."status"), "clients_client"."id" FROM "clients_client" WHERE django_datetime_cast_date("clients_client"."created", "UTC", "UTC") = 2021-10-19 GROUP BY "clients_client"."status"')
        # clients = Client.objects.raw('SELECT DISTINCT ("clients_client"."status"), "clients_client"."id" FROM "clients_client" GROUP BY "clients_client"."status" ')
        for client in clients:
            print("Client: ", client)
        # statuses = Client.objects.filter(created__date=created).values_list('status').distinct().annotate(cant=Count('pk'))
        # print("Status: ", statuses)
        print("Clients: ", clients)
        # print("QueryDesc: ", statuses.query)
        print("QueryDesc: ", clients.query)
        # statuses = Client.objects.filter(created__date=created).values_list('status', flat=True).distinct()
        # for stat in statuses:
        #     print("Stat: ", stat)
        #     clients = Client.objects.filter(created__date=created, status=stat).order_by('pk')
        #     print("Clients:>>> ", clients)
        #     result.append(clients[0])
            
        # clients = Client.objects.filter(created__date=created).values('status').annotate(Count('status'))
        # clients = Client.objects.filter(created__date=created).annotate(Count('status', distinct=True))
        # clients = Client.objects.filter(created__date=created).filter(status__in=[1,2,3,4]).group_by('status').distinct()
        
        return result

    def get(self, request, created):
        clients = self.get_queryset(created)
        if clients:
            print("CLIENTS: ", clients)
            serializer = self.serializer_class(clients, many=True)
            return Response(serializer.data)
        return Response({'status':'Error no clients..!!'})


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
