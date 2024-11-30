from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Aviso
from .forms import AvisoInternoForm, AvisoExternoForm, UserProfileForm

@login_required
def avisos_dashboard(request):
    if request.user.profile.user_type != 'membro':
        return redirect('dashboard')

    # Formulários separados para internos e externos
    form_interno = AvisoInternoForm()
    form_externo = AvisoExternoForm()

    if request.method == 'POST':
        if 'publicar_interno' in request.POST:  # Verifica qual formulário foi submetido
            form_interno = AvisoInternoForm(request.POST)
            if form_interno.is_valid():
                aviso = form_interno.save(commit=False)
                aviso.autor = request.user
                aviso.tipo = 'interno'
                aviso.save()
                return redirect('avisos_dashboard')
        elif 'publicar_externo' in request.POST:
            form_externo = AvisoExternoForm(request.POST)
            if form_externo.is_valid():
                aviso = form_externo.save(commit=False)
                aviso.autor = request.user
                aviso.tipo = 'externo'
                aviso.save()
                return redirect('avisos_dashboard')

    # Listar avisos internos e externos
    avisos_internos = Aviso.objects.filter(tipo='interno').order_by('-data_criacao')
    avisos_externos = Aviso.objects.filter(tipo='externo').order_by('-data_criacao')

    context = {
        'form_interno': form_interno,
        'form_externo': form_externo,
        'avisos_internos': avisos_internos,
        'avisos_externos': avisos_externos,
    }
    #print(form_interno.as_table())
    #print(form_interno.errors)
    
    if request.user.profile.user_type == "candidato":
        context['avisos'] = avisos_externos

    return render(request, 'dashboard.html', context)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            print("Erros no formulário:", form.errors)
            error_messages = [
                {"label": form.fields[field].label, "errors": form.errors[field]}
                for field in form.errors
            ]
    else:
        form = CustomUserCreationForm()
        error_messages = []

    return render(request, 'accounts/signup.html', {
        'form': form,
        'error_messages': error_messages,
    })

@login_required
def dashboard(request):
    context = {}

    if request.user.profile.user_type == "candidato":
        avisos_externos = Aviso.objects.filter(tipo='externo').order_by('-data_criacao')
        context['avisos'] = avisos_externos

    return render(request, 'dashboard.html', context)

@login_required
def palestras(request):
    return render(request, 'palestras.html')

@login_required
def dinamicas(request):
    return render(request, 'dinamicas.html')

@login_required
def entrevistas(request):
    return render(request, 'entrevistas.html')

@login_required
def meu_perfil(request):
    user_profile = request.user.profile
    return render(request, 'meu_perfil.html', {'user_profile': user_profile})

@login_required
def editar_perfil(request):
    # Obtém o perfil do usuário autenticado
    user_profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()  # Salva as alterações no banco de dados
            return redirect('meu_perfil')  # Redireciona para a página de perfil após salvar
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'editar_perfil.html', {'form': form})
