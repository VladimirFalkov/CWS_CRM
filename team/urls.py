from django.urls import path

from .views import edit_team, detail, teams_list, teams_activate


app_name = 'team'

urlpatterns = [
    path('', teams_list, name='list'),
    path('<int:pk>/', detail, name='detail'),
    path('<int:pk>/edit/', edit_team, name='edit'),
    path('<int:pk>/activate/', teams_activate, name='activate'),
]