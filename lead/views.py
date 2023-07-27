from typing import Any, Dict
from django.contrib import messages 
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404 #, render 
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.views import View
from django.urls import reverse_lazy
#from django.utils.decorators import method_decorator

from .forms import AddCommentForm, AddFileForm
from .models import Lead, Comment
from client.models import Client, Comment as ClientComment
from team.models import Team



class LeadListView(LoginRequiredMixin, ListView):
    model = Lead

# Changed this dispatch on LoginRequiredMixin everywhere in views

    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
        #return super().dispatch(*args, **kwargs)


    def get_queryset(self):
        queryset = super(LeadListView,self).get_queryset()

        return queryset.filter(created_by=self.request.user, converted_to_client=False)

        

#@login_required
#def leads_list(request):
    #leads = Lead.objects.filter(created_by=request.user, converted_to_client=False)
    #return render(request, 'lead/lead_list.html', {'leads': leads})


class LeadDeleteView(LoginRequiredMixin,DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')


    def get_queryset(self):
        queryset = super(LeadDeleteView,self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request,*args, **kwargs)

# @login_required
# def leads_delete(request, pk):
    # lead = get_object_or_404(Lead, pk=pk, created_by=request.user)
    # lead.delete()

    # messages.success(request, 'The lead was deleted')

    # return redirect('leads:list')

class LeadCreateView(LoginRequiredMixin,CreateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('leads:list')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.request.user.userprofile.active_team
        context['team'] = team
        context['title'] = 'Add new lead'

        return context

    
    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = self.request.user.userprofile.active_team
        self.object.save()
        
        return redirect(self.get_success_url())


#@login_required
#def add_lead(request):
 #   team = Team.objects.filter(created_by=request.user)[0]
#
#
    #if request.method == "POST":
        #form = AddLeadForm(request.POST)
        #if form.is_valid():
#
        #    team = Team.objects.filter(created_by=request.user)[0]
        #    lead = form.save(commit=False)
        #    lead.created_by = request.user
        #    lead.team = team
        #    lead.save()
#
        #    messages.success(request, 'The lead was created')
#
        #    return redirect('leads:list')
    #else:
    #    form = AddLeadForm()
    #return render(request, 'lead/add_lead.html', {
    #    'form': form,
    #    'team': team
    #})



class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()

        return context

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))



#@login_required
#def leads_detail(request, pk):
    #lead = get_object_or_404(Lead, pk=pk, created_by=request.user)

    #return render(request, 'lead/lead_detail.html',{
        #'lead': lead
    #})


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('leads:list')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update lead'

        return context

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    

#@login_required
#def leads_edit(request, pk):
 #   lead = get_object_or_404(Lead, pk=pk, created_by=request.user)

    #if request.method == "POST":
        #form = AddLeadForm(request.POST, instance=lead)

        #if form.is_valid():
            #form.save()

            #messages.success(request, 'The lead was updated')
        #
        #return redirect('leads:list')
    #else:
        #form = AddLeadForm(instance=lead)
#
    #return render(request, 'lead/leads_edit.html',{
        #'form': form
    #})

class ConvertToClientView(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        lead = get_object_or_404(Lead, pk=pk, created_by=request.user)
        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            team = self.request.user.userprofile.active_team,
        )
        lead.converted_to_client = True
        lead.save()

        # Convert lead`s comments to client`s comments
        comments = Comment.objects.all()

        for comment in comments:
            ClientComment.objects.create(
                content = comment.content,
                client = client,
                created_by = comment.created_by,
                team = self.request.user.userprofile.active_team

            )
        # Show message and redirect


        messages.success(request, 'The lead was converted to a client.')
        
        return redirect('leads:list')
    
#def convert_to_client(request, pk):
    #lead = get_object_or_404(Lead, pk=pk, created_by=request.user)
    #team = Team.objects.filter(created_by=request.user)[0]


    #client = Client.objects.create(
        #name=lead.name,
        #email=lead.email,
        #description=lead.description,
        #created_by=request.user,
        #team = team,
    #)
    #lead.converted_to_client = True
    #lead.save()
    #messages.success(request, 'The lead was converted to a client.')

    #return redirect('leads:list')

class AddFileView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            team = self.request.user.userprofile.active_team
            file = form.save(commit=False)
            file.team = team
            file.lead_id = pk
            file.created_by = request.user 
            file.save()
            
        return redirect('leads:detail', pk=pk)

class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form = AddCommentForm(request.POST)
        
        if form.is_valid():
            team = self.request.user.userprofile.active_team
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()

        return redirect('leads:detail', pk=pk)