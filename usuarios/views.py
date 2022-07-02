from django.contrib import auth, messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.

def login(request):             #Login e validação
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
            messages.info(request, 'Email ou senha incorreto.')
            return redirect('login')
        
        auth.login(request, user)
        return redirect('/')

def logout(request):            #Logout e destruição da sessão
    request.session.flush()
    return redirect('login')
