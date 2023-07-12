from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from client.models import Client
from lead.models import Lead
from team.models import Team

@login_required
def dashboard(request):
    team = Team.objects.filter(created_by=request.user)[0]

    leads = Lead.objects.filter(team=team, converted_to_client=False).order_by('-created_at')
    clients = Client.objects.filter(team=team).order_by('-created_at')
    return render(request, 'dashboard/dashboard.html', {
        'leads': leads,
        'clients': clients,
    })