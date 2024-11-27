from django.urls import path

from . import views

app_name = 'palestras'
urlpatterns = [
    path('', views.list_palestras, name='index'),
    path('select/', views.select_palestra, name='select'),
]