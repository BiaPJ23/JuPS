from django.contrib import admin
from .models import Disponibilidade, Dinamica

@admin.register(Disponibilidade)
class DisponibilidadeAdmin(admin.ModelAdmin):
    list_display = ('membro', 'data', 'hora')

@admin.register(Dinamica)
class DinamicaAdmin(admin.ModelAdmin):
    list_display = ('horario', )
    filter_horizontal = ('candidatos',)