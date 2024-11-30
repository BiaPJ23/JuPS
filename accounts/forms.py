from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Aviso

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="Nome completo",
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome completo'}),
    )
    curso = forms.CharField(max_length=100, required=True, label="Curso")
    ano_ingresso = forms.IntegerField(required=True, label="Ano de Ingresso")
    genero = forms.ChoiceField(
        choices=[
            ('masculino', 'Masculino'),
            ('feminino', 'Feminino'),
            ('nao-binario', 'Não-binário'),
            ('prefiro-nao-dizer', 'Prefiro não dizer'),
        ],
        label="Gênero",
    )
    data_nascimento = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data de Nascimento"
    )
    telefone = forms.CharField(max_length=15, required=True, label="Telefone")

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Nome completo
        full_name = self.cleaned_data.get('full_name').strip()
        if " " in full_name:
            user.first_name, user.last_name = full_name.split(" ", 1)
        else:
            user.first_name = full_name
            user.last_name = ""
        if commit:
            user.save()
            # Criar perfil de usuário com os dados extras
            UserProfile.objects.create(
                user=user,
                curso=self.cleaned_data.get('curso'),
                ano_ingresso=self.cleaned_data.get('ano_ingresso'),
                genero=self.cleaned_data.get('genero'),
                data_nascimento=self.cleaned_data.get('data_nascimento'),
                telefone=self.cleaned_data.get('telefone'),
            )
        return user


class AvisoInternoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',  
                'rows': 4,  
                'placeholder': 'Digite o aviso interno aqui...',  
            }),
        }

class AvisoExternoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Digite o aviso externo aqui...',
            }),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['curso', 'ano_ingresso', 'genero', 'data_nascimento', 'telefone']  # Campos que o usuário pode editar

        # Adicionando labels personalizados, se necessário
        labels = {
            'curso': 'Curso de Ingresso',
            'ano_ingresso': 'Ano de Ingresso',
            'genero': 'Gênero',
            'data_nascimento': 'Data de Nascimento',
            'telefone': 'Telefone de Contato',
        }
