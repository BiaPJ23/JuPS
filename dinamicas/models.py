from django.db import models
from django.contrib.auth.models import User

class Disponibilidade(models.Model):
    membro = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disponibilidades')
    data = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.membro.username} - {self.data} às {self.hora}"

class Dinamica(models.Model):
    horario = models.OneToOneField(Disponibilidade, on_delete=models.CASCADE, related_name='dinamica')
    candidatos = models.ManyToManyField(User, related_name='dinamicas')

    def __str__(self):
        return f"Dinamica em {self.horario.data} às {self.horario.hora}"
    

class ForumDinamica(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuário que publicou a mensagem
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.autor.username} - {self.texto[:20]}'