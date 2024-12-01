from django.urls import path
from . import views

urlpatterns = [
    path('', views.entrevistas, name='entrevistas'),  
    path('aprovar-entrevistas/', views.aprovar_entrevistas, name='aprovar_entrevistas'),
    path('chat-duvidas/', views.chat_duvidas, name='chat_duvidas'),
]