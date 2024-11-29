from django.urls import path
from . import views

urlpatterns = [
    path('', views.dinamicas, name='dinamicas'),  
]