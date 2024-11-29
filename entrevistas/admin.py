from django.contrib import admin
from .models import DisponibilidadeEntrevista, Entrevista

@admin.register(DisponibilidadeEntrevista)
class DisponibilidadeEntrevistaAdmin(admin.ModelAdmin):
    list_display = ('membro', 'data', 'hora')

@admin.register(Entrevista)
class EntrevistaAdmin(admin.ModelAdmin):
    list_display = ('horario', )
    filter_horizontal = ('candidatos',)