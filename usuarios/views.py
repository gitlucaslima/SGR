from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from rolepermissions.decorators import has_permission_decorator

# Create your views here.

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    elif request.method == "POST":
        login = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)
        

        if not user:
            #TODO: redirecionar com mensagem de erro
            return HttpResponse('Usuário inválido')
        
        auth.login(request, user)
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('login')
