from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddClientForm

from .models import Client
from team.models import Team


@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)

    return render(request,'client/clients_list.html', {
        'clients': clients
        })


@login_required
def clients_detail(request, pk):
    client = get_object_or_404(Client, pk=pk, created_by=request.user)

    return render(request, 'client/clients_detail.html',{
        'client': client
    })


@login_required
def add_client(request):
    team = Team.objects.filter(created_by=request.user)[0]


    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()

            messages.success(request, 'The client was created')

            return redirect('clients:list')
    else:
        form = AddClientForm()
    return render(request, 'client/add_client.html', {
        'form': form,
        'team': team
    })


@login_required
def clients_delete(request, pk):
    client = get_object_or_404(Client, pk=pk, created_by=request.user)
    client.delete()

    messages.success(request, 'The client was deleted')

    return redirect('clients:list')


@login_required
def clients_edit(request, pk):
    client = get_object_or_404(Client, pk=pk, created_by=request.user)

    if request.method == "POST":
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(request, 'The client was updated')
        
        return redirect('clients:list')
    else:
        form = AddClientForm(instance=client)

    return render(request, 'client/clients_edit.html',{
        'form': form
    })
