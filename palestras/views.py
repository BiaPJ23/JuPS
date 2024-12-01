from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Palestra, Selecao
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import UserProfile

# Create your views here.
def list_palestras(request):
    palestra_list = Palestra.objects.all()
    context = {'palestra_list': palestra_list}
    return render(request, 'palestras/index.html', context)

@login_required
def select_palestra(request):
    if request.method == 'POST':
        palestra_id = request.POST.get('palestra_id')
        palestra = get_object_or_404(Palestra, id=palestra_id)
        if Selecao.objects.filter(user=request.user).exists():
            message = "Você já selecionou uma palestra. Não é possível escolher outra."
        else:
            Selecao.objects.create(user=request.user, palestra=palestra)
            message = f'Você selecionou a palestra: {palestra.name} no horário {palestra.horário}.'
        palestra_list = Palestra.objects.all()
        context = {
            'palestra_list': palestra_list,
            'message': message
        }
        return render(request, 'palestras/index.html', context)
    return HttpResponseRedirect(reverse('palestras:index'))

@login_required
def aprovar_palestras(request):
    if request.user.profile.user_type != 'membro':
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('dashboard')

    candidatos = UserProfile.objects.filter(user_type='candidato')

    if request.method == 'POST':
        for candidato in candidatos:
            novo_status = request.POST.get(f'status_{candidato.id}')
            if novo_status:
                candidato.status_palestra = novo_status
                candidato.save()
        messages.success(request, "Status das palestras atualizado com sucesso!")
        return redirect('palestras:aprovar_palestras')

    return render(request, 'aprovar_palestras.html', {'candidatos': candidatos})
