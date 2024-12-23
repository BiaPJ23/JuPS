from django.urls import path
from accounts import views
from . import views

urlpatterns = [
    path('', views.list_palestras, name='palestras'),
    path('select/', views.select_palestra, name='select'),
    path('aprovar-palestras/', views.aprovar_palestras, name='aprovar_palestras'),
    path('chat-duvidas/', views.chat_duvidas, name='chat_duvidas'),
]