from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserProfile(models.Model):
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

    feedback_dinamica = models.TextField(null=True, blank=True)
    feedback_entrevista = models.TextField(null=True, blank=True)
    
    USER_TYPES = (
        ('membro', 'Membro'),
        ('candidato', 'Candidato'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPES, 
        default='candidato', 
        verbose_name="Tipo de Usuário")
    
    APROVACAO_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('reprovado', 'Reprovado'),
    ]
    status_dinamica = models.CharField(
        max_length=10, 
        choices=APROVACAO_CHOICES, 
        default='pendente', 
        verbose_name="Status Dinâmica"
    )

    status_entrevista = models.CharField(
        max_length=10, 
        choices=APROVACAO_CHOICES, 
        default='pendente', 
        verbose_name="Status Entrevista"
    )

    status_palestra = models.CharField(
        max_length=10, 
        choices=APROVACAO_CHOICES, 
        default='pendente', 
        verbose_name="Status Palestra"
    )


    def __str__(self):
        return f"Perfil de {self.user.username}"

class Aviso(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuário que publicou o aviso
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(
        max_length=10,
        choices=[('interno', 'Interno'), ('externo', 'Externo')],
        default='externo',
    )

    def __str__(self):
        return f"{self.tipo.capitalize()} - {self.conteudo[:20]}..."
    
class MensagemChat(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    mensagem = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.first_name}: {self.mensagem[:30]}..."
