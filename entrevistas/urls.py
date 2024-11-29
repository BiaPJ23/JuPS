from django.urls import path
from . import views

urlpatterns = [
    path('', views.entrevistas, name='entrevistas'),  
]