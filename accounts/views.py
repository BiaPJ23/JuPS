from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib import messages

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