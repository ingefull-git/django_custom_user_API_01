from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.clients.models import Client, Status


@login_required
def clients_list_view(request):
    status = [stat for stat in Status.labels]
    print("Status: ", status)
    context = {
        'status': status
    }
    return render(request, 'list.html', context)