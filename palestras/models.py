from django.db import models
from django.conf import settings
# Create your models here.

class Palestra(models.Model):
    name = models.CharField(max_length=255)
    horário = models.DateTimeField()

    def __str__(self):
        return f'{self.name} ({self.horário})'

class Selecao(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    palestra = models.ForeignKey(Palestra, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} selecionou {self.palestra}'