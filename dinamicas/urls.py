from django.urls import path
from . import views

urlpatterns = [
    path('', views.dinamicas, name='dinamicas'),  
    path('aprovar-dinâmicas/', views.aprovar_dinamicas, name='aprovar_dinamicas'),
]