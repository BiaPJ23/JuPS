from django.urls import path
from . import views

urlpatterns = [
    path('', views.dinamicas, name='dinamicas'),  
    path('aprovar-candidatos/', views.aprovar_candidatos, name='aprovar_candidatos'),
]