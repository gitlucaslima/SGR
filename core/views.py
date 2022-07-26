from django.shortcuts import redirect, render

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

    return render(request, "coordenador/home.html")


# Controller do configuraçoes

def configuracoes(request,relatorio):

    contexto = {
        "tab":relatorio
    }
    if relatorio == 'usuario':

        dados = UsuarioModel.objects.all()
        dados_modificados = []
        for usuario in dados:

            usuario_modificado = {
                "nome":usuario.nome,
                "email":usuario.email,
                "status":usuario.status
            }
            teste = usuario is AlunoModel
            print(teste,type(usuario))
            if teste :
                print("testasdasda")
                usuario_modificado['permissao'] = "Aluno"

            dados_modificados.append(usuario_modificado) 
        contexto['dados_usuarios'] = dados_modificados


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
 
<<<<<<< HEAD
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

=======
>>>>>>> 23ff66405bb1ab4d97804f0d758152c7a3a03e2a
