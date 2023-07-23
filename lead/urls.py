from django.urls import path

from . import views

app_name = 'leads'
urlpatterns = [
    # functions view - path('', views.leads_list, name='list'),
    path('', views.LeadListView.as_view(), name='list'),
    # functions view - path('<int:pk>/', views.leads_detail, name='detail'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='detail'),
    path("<int:pk>/delete/", views.LeadDeleteView.as_view(), name='delete'),
    # functions view - path("<int:pk>/delete/", views.leads_delete, name='delete'),
    path('<int:pk>/edit/', views.LeadUpdateView.as_view(), name='edit'),
    #path('<int:pk>/edit/', views.leads_edit, name='edit'),
    #path('<int:pk>/convert/', views.convert_to_client, name='convert'),
    path('<int:pk>/convert/', views.ConvertToClientView.as_view(), name='convert'),
    path('<int:pk>/add-comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('<int:pk>/add-file/', views.AddFileView.as_view(), name='add_file'),
    path('add/', views.LeadCreateView.as_view(), name='add'),
    #path('add-lead/', views.add_lead, name='add'),
    
]