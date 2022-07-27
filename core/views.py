from django.shortcuts import get_object_or_404, redirect, render

from core.models import *

# Controllers do aluno


def alunoHome(request):

    return render(request, "aluno/home.html")


def alunoRelatorio(request):

    return render(request, "aluno/gerarRelatorio.html")


# Controller do tutor
def tutorHome(request):

    return render(request, "tutor/home.html")


# Controller do coordenador

def coordenadorHome(request):

    dados = UsuarioModel.objects.all()
    numeroAlunos = UsuarioModel.objects.filter(permissao=1).count()

    contexto = {
        "tab":dados,
        "numeroAlunos": numeroAlunos,
    }

    contexto['dados_usuarios'] = dados

    return render(request, "coordenador/home.html", contexto)


# Controller do configuraçoes

def configuracoes(request, relatorio):

    contexto = {
        "tab":relatorio
    }
    if relatorio == 'usuario':

        dados = UsuarioModel.objects.all()
   
        contexto['dados_usuarios'] = dados

    return render(request, "configuracoes/configuracoesCoordenador.html",contexto)


# Controller do avisos

def avisos(request):

    return render(request, "avisos/avisosAluno.html")

# Controller do login

def login(request):

    return render(request, 'partius/gerenciarAcesso/login.html')


# Controller do registro

def registro(request):

    return render(request, 'partius/gerenciarAcesso/registro.html')


# Controller do registro

def redefine_senha(request):

    return render(request, 'partius/gerenciarAcesso/redefinicaoSenha.html')
 
# Cadastro de usuarios

def cadastroUsuario(request):

    if request.method == "POST":

        nome = request.POST.get("nome")
        email = request.POST.get("email")
        permissao = request.POST.get("permissao")

        
        if(permissao == '1'):
            
            novo_usuario = AlunoModel()
            novo_usuario.nome = nome
            novo_usuario.email = email
            novo_usuario.permissao = 1

        elif permissao == '2':
            novo_usuario = TutorModel()
            novo_usuario.nome = nome
            novo_usuario.email = email
            novo_usuario.permissao = 2

        else:
            novo_usuario = CoordenadorModel()
            novo_usuario.nome = nome
            novo_usuario.email = email
            novo_usuario.permissao = 3


        novo_usuario.save()
      

    return redirect("/configuracoes/usuario")

def editaUsuario(request, id):

    print(request)

    if request.method == "POST":

        instance = UsuarioModel.objects.filter(id=id).first()
        
        instance.nome = request.POST.get("nome")
        instance.email = request.POST.get("email")
        instance.permissao = request.POST.get("permissao")

        instance.save()    

    return redirect("/configuracoes/usuario")


def deletaUsuario(request, id):
    
    instance = get_object_or_404(UsuarioModel, id=id)
    instance.delete()   

    return redirect("/configuracoes/usuario")
