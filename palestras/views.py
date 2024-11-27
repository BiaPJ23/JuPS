from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Palestra, Selecao

# Create your views here.
def list_palestras(request):
    palestra_list = Palestra.objects.all()
    context = {'palestra_list': palestra_list}
    return render(request, 'palestras/index.html', context)

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


