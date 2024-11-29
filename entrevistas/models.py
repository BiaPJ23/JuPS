from django.db import models
from django.contrib.auth.models import User

class DisponibilidadeEntrevista(models.Model):
    membro = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disponibilidades_entrevista')
    data = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.membro.username} - {self.data} às {self.hora}"

class Entrevista(models.Model):
    horario = models.OneToOneField(DisponibilidadeEntrevista, on_delete=models.CASCADE, related_name='entrevista')
    candidatos = models.ManyToManyField(User, related_name='entrevistas')

    def __str__(self):
        return f"Entrevista em {self.horario.data} às {self.horario.hora}"