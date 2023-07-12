
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

from core.views import index, about
from userprofile.views import signup, myaccount
urlpatterns = [
    path('', index, name='index'),
    path('dashboard/leads/', include('lead.urls')),
    path('dashboard/clients/', include('client.urls')),
    path('dashboard/myaccount/', myaccount, name='myaccount'),
    path('dashboard/teams/', include('team.urls')),
    path('dashboard/', include('dashboard.urls')),
    path("admin/", admin.site.urls),
    path("about/", about, name='about'),
    path("signup/", signup, name='signup'),
    path('login/', views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

]