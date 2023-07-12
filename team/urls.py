from django.urls import path

from .views import edit_team


urlpatterns = [
    path('<int:pk>/edit/', edit_team, name='edit_team'),
]