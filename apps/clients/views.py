from django.db import connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.clients.models import Client, Invoice, Status


def dictfetchall(cursor):
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()
    ]


@login_required
def clients_list_view(request):
    status = [stat for stat in Status.choices]
    print("Status: ", status)
    # clients = Client.objects.all()
    cursor = connection.cursor()
    cursor.execute("SELECT clients_client.status, COUNT(clients_client.id) AS cant FROM clients_client GROUP BY clients_client.status")
    clients = dictfetchall(cursor)
    invoices = Invoice.objects.all()
    context = {
        'status': status,
        'invoices': invoices
    }
    return render(request, 'list.html', context)