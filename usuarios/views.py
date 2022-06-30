from django.contrib import auth
from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from rolepermissions.decorators import has_permission_decorator

from .models import Users

# Create your views here.

@has_permission_decorator('cadastrar_tutor')
def cadastrar_tutor(request):
    if request.method == "GET":
        return render(request, 'cadastrar_tutor.html')
    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = Users.objects.filter(email=email)

        if user.exists():
            #TODO: utilizar messages do Django
            return HttpResponse('Email já existe.')
        
        user = Users.objects.create_user(username=email, email=email, password=senha, funcao="T")

        #TODO: Redirecionar com message
        return HttpResponse('Conta Criada')

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('plataforma'))
        return render(request, 'login.html')
    elif request.method == "POST":
        login = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)

        if not user:
            #TODO: redirecionar com mensagem de erro
            return HttpResponse('Usuário inválido')
        
        auth.login(request, user)
        return HttpResponse('Usuario logado com sucesso')

def logout(request):
    request.session.flush()
    return redirect(reverse('login'))
