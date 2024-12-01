from django.shortcuts import render, redirect
from .models import DisponibilidadeEntrevista, Entrevista
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import UserProfile
from accounts.models import MensagemChat
from accounts.forms import ChatForm

@login_required
def entrevistas(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.user.profile.user_type == 'membro':
        if request.method == 'POST':
            disponibilidades_entrevistas = request.POST.getlist('disponibilidades_entrevistas[]')
            for item in disponibilidades_entrevistas:
                data, hora = item.split('|')
                DisponibilidadeEntrevista.objects.get_or_create(
                    membro=request.user,
                    data=datetime.strptime(data, '%d/%m/%Y').date(),
                    hora=datetime.strptime(hora, '%H:%M').time()
                )

            messages.success(request, "Disponibilidades salvas com sucesso!")
            return redirect('entrevistas')

        # Verificar disponibilidades já cadastradas
        disponibilidades_existentes = DisponibilidadeEntrevista.objects.filter(membro=request.user)
        if disponibilidades_existentes.exists():
            mensagens_disponibilidades = [
                f"{disp.data.strftime('%d/%m/%Y')} às {disp.hora.strftime('%H:%M')}" 
                for disp in disponibilidades_existentes
            ]
            return render(request, 'entrevistas.html', {
                'mensagem': f"Você já selecionou suas disponibilidades: {', '.join(mensagens_disponibilidades)}.",
                'is_membro': True
            })

        # Caso não existam disponibilidades, exibir opções para configurar
        datas = [datetime(2024, 9, 1) + timedelta(days=i) for i in range(7)]
        horarios = ['15:00', '16:00', '17:00', '18:00', '19:00', '20:00']
        return render(request, 'entrevistas.html', {'datas': datas, 'horarios': horarios, 'is_membro': True})

    elif request.user.profile.user_type == 'candidato':
        # Verificar se o candidato já está inscrito
        entrevistas_inscrito = request.user.entrevistas.all()
        if entrevistas_inscrito.exists():
            entrevista = entrevistas_inscrito.first()
            mensagem_inscricao = (
                f"Você já está inscrito na entrevista do dia "
                f"{entrevista.horario.data.strftime('%d/%m/%Y')} às {entrevista.horario.hora.strftime('%H:%M')}."
            )
            return render(request, 'entrevistas.html', {
                'mensagem': mensagem_inscricao,
                'is_membro': False,
                'user_profile': user_profile
            })

        if request.method == 'POST':
            disponibilidade_entrevista_id = request.POST.get('disponibilidade_entrevista_id')
            try:
                disponibilidade_entrevista = DisponibilidadeEntrevista.objects.get(id=disponibilidade_entrevista_id)
            
                # Verifique se a dinâmica já existe, e se não estiver cheia
                if not hasattr( disponibilidade_entrevista, 'entrevista'):
                    entrevista = Entrevista.objects.create(horario=disponibilidade_entrevista)
                    disponibilidade_entrevista.entrevista = entrevista
                    disponibilidade_entrevista.save()

                if  disponibilidade_entrevista.entrevista.candidatos.count() < 1:
                    disponibilidade_entrevista.entrevista.candidatos.add(request.user)
                    messages.success(request, 
                        f"Inscrição realizada com sucesso! Você está inscrito na entrevista do dia "
                        f"{disponibilidade_entrevista.data.strftime('%d/%m/%Y')} às {disponibilidade_entrevista.hora.strftime('%H:%M')}."
                    )
                else:
                    messages.error(request, "Esse horário já está cheio!")
            except DisponibilidadeEntrevista.DoesNotExist:
                messages.error(request, "Horário inválido!")
            return redirect('entrevistas')

        # Exibir horários disponíveis
        disponibilidades_entrevistas = DisponibilidadeEntrevista.objects.filter(entrevista__isnull=True).order_by('data', 'hora')
        return render(request, 'entrevistas.html', {
            'disponibilidades_entrevistas': disponibilidades_entrevistas, 
            'is_membro': False,
            'user_profile': user_profile
            })
    
    else:
        # Redirecionar se o user_type não for membro nem candidato
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('dashboard')

@login_required
def aprovar_entrevistas(request):
    if request.user.profile.user_type != 'membro':
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('dashboard')

    candidatos = UserProfile.objects.filter(user_type='candidato', status_dinamica='aprovado')

    if request.method == 'POST':
        for candidato in candidatos:
            novo_status = request.POST.get(f'status_{candidato.id}')
            if novo_status:
                candidato.status_entrevista = novo_status
                candidato.save()
        messages.success(request, "Status das entrevistas atualizado com sucesso!")
        return redirect('aprovar_entrevistas')

    return render(request, 'aprovar_entrevistas.html', {'candidatos': candidatos})


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
    return render(request, 'palestras/chat_palestras.html', context)