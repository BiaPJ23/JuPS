from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('avisos_dashboard/', views.avisos_dashboard, name='avisos_dashboard'),
    path('palestras/', views.palestras, name='palestras'),
    path('dinamicas/', views.dinamicas, name='dinamicas'),
    path('entrevistas/', views.entrevistas, name='entrevistas'),
    path('meu_perfil/', views.meu_perfil, name='meu_perfil'),
]