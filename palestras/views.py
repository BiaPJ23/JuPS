from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Palestra, Selecao
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import UserProfile
from accounts.models import MensagemChat
from accounts.forms import ChatForm

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

@login_required
def chat_duvidas(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.autor = request.user
            mensagem.save()
            messages.success(request, "Sua mensagem foi enviada!")
            return redirect('palestras:chat_duvidas')
    else:
        form = ChatForm()

    mensagens = MensagemChat.objects.all().order_by('-data_hora')  # Mensagens mais recentes primeiro
    context = {
        'form': form,
        'mensagens': mensagens,
    }
    return render(request, 'palestras/chat_duvidas.html', context)