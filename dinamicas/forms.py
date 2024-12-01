from django import forms
from .models import ForumDinamica

class DuvidasDinamicas(forms.ModelForm):
    class Meta:
        model = ForumDinamica
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',  
                'rows': 4,  
                'placeholder': 'Digite sua dúvida aqui...',  
            }),
        }