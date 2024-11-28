from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Relaciona com o modelo User padrão
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Campos adicionais
    curso = models.CharField(max_length=100, verbose_name="Curso")
    ano_ingresso = models.PositiveIntegerField(verbose_name="Ano de Ingresso")
    genero = models.CharField(
        max_length=20,
        choices=[
            ('masculino', 'Masculino'),
            ('feminino', 'Feminino'),
            ('nao-binario', 'Não-binário'),
            ('prefiro-nao-dizer', 'Prefiro não dizer'),
        ],
        verbose_name="Gênero"
    )
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")

    def __str__(self):
        return f"Perfil de {self.user.username}"
