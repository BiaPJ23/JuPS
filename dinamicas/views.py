from django.shortcuts import render, redirect
from .models import Disponibilidade, Dinamica
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import UserProfile

@login_required
def dinamicas(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.user.profile.user_type == 'membro':
        if request.method == 'POST':
            disponibilidades = request.POST.getlist('disponibilidades[]')
            for item in disponibilidades:
                data, hora = item.split('|')
                Disponibilidade.objects.get_or_create(
                    membro=request.user,
                    data=datetime.strptime(data, '%d/%m/%Y').date(),
                    hora=datetime.strptime(hora, '%H:%M').time()
                )

            messages.success(request, "Disponibilidades salvas com sucesso!")
            return redirect('dinamicas')

        # Verificar disponibilidades já cadastradas
        disponibilidades_existentes = Disponibilidade.objects.filter(membro=request.user)
        if disponibilidades_existentes.exists():
            mensagens_disponibilidades = [
                f"{disp.data.strftime('%d/%m/%Y')} às {disp.hora.strftime('%H:%M')}" 
                for disp in disponibilidades_existentes
            ]
            return render(request, 'dinamicas.html', {
                'mensagem': f"Você já selecionou suas disponibilidades: {', '.join(mensagens_disponibilidades)}.",
                'is_membro': True
            })

        # Caso não existam disponibilidades, exibir opções para configurar
        datas = [datetime(2024, 8, 14) + timedelta(days=i) for i in range(7)]
        horarios = ['15:00', '16:00', '17:00', '18:00', '19:00', '20:00']
        return render(request, 'dinamicas.html', {'datas': datas, 'horarios': horarios, 'is_membro': True})

    elif request.user.profile.user_type == 'candidato':
        # Verificar se o candidato já está inscrito
        status_dinamica = request.user.profile.status_dinamica

        dinamicas_inscrito = request.user.dinamicas.all()
        if dinamicas_inscrito.exists():
            dinamica = dinamicas_inscrito.first()
            mensagem_inscricao = (
                f"Você já está inscrito na dinâmica do dia "
                f"{dinamica.horario.data.strftime('%d/%m/%Y')} às {dinamica.horario.hora.strftime('%H:%M')}."
            )
            return render(request, 'dinamicas.html', {
                'mensagem': mensagem_inscricao,
                'is_membro': False,
                'user_profile': user_profile
            })

        if request.method == 'POST':
            disponibilidade_id = request.POST.get('disponibilidade_id')
            try:
                disponibilidade = Disponibilidade.objects.get(id=disponibilidade_id)
            
                # Verifique se a dinâmica já existe, e se não estiver cheia
                if not hasattr(disponibilidade, 'dinamica'):
                    dinamica = Dinamica.objects.create(horario=disponibilidade)
                    disponibilidade.dinamica = dinamica
                    disponibilidade.save()

                if disponibilidade.dinamica.candidatos.count() < 5:
                    disponibilidade.dinamica.candidatos.add(request.user)
                    messages.success(request, 
                        f"Inscrição realizada com sucesso! Você está inscrito na dinâmica do dia "
                        f"{disponibilidade.data.strftime('%d/%m/%Y')} às {disponibilidade.hora.strftime('%H:%M')}."
                    )
                else:
                    messages.error(request, "Esse horário já está cheio!")
            except Disponibilidade.DoesNotExist:
                messages.error(request, "Horário inválido!")
            return redirect('dinamicas')

        # Exibir horários disponíveis
        disponibilidades = Disponibilidade.objects.filter(dinamica__isnull=True).order_by('data', 'hora')
        return render(request, 'dinamicas.html', {
            'disponibilidades': disponibilidades, 
            'is_membro': False,
            'user_profile': user_profile
            })
    
    else:
        # Redirecionar se o user_type não for membro nem candidato
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('dashboard')
    
@login_required
def aprovar_dinamicas(request):
    if request.user.profile.user_type != 'membro':
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('dashboard')

    candidatos = UserProfile.objects.filter(user_type='candidato', status_palestra='aprovado')

    if request.method == 'POST':
        for candidato in candidatos:
            novo_status = request.POST.get(f'status_{candidato.id}')
            if novo_status:
                candidato.status_dinamica = novo_status
                candidato.save()
        messages.success(request, "Status das dinâmicas atualizado com sucesso!")
        return redirect('aprovar_dinamicas')

    return render(request, 'aprovar_dinamicas.html', {'candidatos': candidatos})

