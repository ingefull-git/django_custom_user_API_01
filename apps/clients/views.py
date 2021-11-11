from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.clients.models import Client, Invoice, Status


@login_required
def clients_list_view(request):
    status = Status
    invoices = Invoice.objects.all().select_related('client')
    # invoices = Invoice.objects.all()
        
    context = {
        'status': status,
        'invoices': invoices
    }
    return render(request, 'list.html', context)