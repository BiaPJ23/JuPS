from django.urls import path
from accounts import views
from . import views

app_name = 'dinamicas'

urlpatterns = [
    path('', views.dinamicas, name='dinamicas'),  
    path('aprovar-dinâmicas/', views.aprovar_dinamicas, name='aprovar_dinamicas'),
    path('chat-duvidas/', views.chat_duvidas, name='chat_duvidas'),
]