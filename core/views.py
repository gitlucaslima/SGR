from datetime import datetime
import io
from msilib.schema import Error
import sys
from tkinter import OUTSIDE

from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile
from core.funcoes_auxiliares.data import isDateMaior
from core.models import *
from PIL import Image
from io import BytesIO
import base64

# Controllers do aluno


def alunoHome(request):

    context = {

        "url": "aluno_home"

    }
    return render(request, "aluno/home.html",context)


def alunoRelatorio(request):

    return render(request, "aluno/gerarRelatorio.html")


# Controller do tutor
def tutorHome(request):

    context = {

        "url": "tutor_home"

    }
    return render(request, "tutor/home.html",context)


# Controller do coordenador

def coordenadorHome(request):

    dados = UsuarioModel.objects.filter(permissao=1)
    

    contexto = {
        "tab":dados,
        "numeroAlunos": dados.count()
        
    }

    contexto['dados_usuarios'] = dados

    return render(request, "coordenador/home.html", contexto)


# Controller do configuraçoes

def configuracoes(request, relatorio):

    disciplinas = DisciplinaModel.objects.filter(status = 1)

    contexto = {
        "tab":relatorio,
        "disciplinas":disciplinas
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

    if request.method == "POST":

        instance = UsuarioModel.objects.filter(id=id).first()
        
        instance.nome = request.POST.get("nome")
        instance.email = request.POST.get("email")
        instance.permissao = request.POST.get("permissao")
        instance.status = request.POST.get("status")
        print(request.POST.get("status"))

        instance.save()    

    return redirect("/configuracoes/usuario")


def deletaUsuario(request):

    if request.method == 'POST':
        
        id = request.POST.get('id')
        instance = get_object_or_404(UsuarioModel, id = id)
        instance.delete()

    return redirect("/configuracoes/usuario")


def cadastrarDisciplina(request):

    if(request.method == "POST"):

        nome = request.POST.get("nome")
        dataInicio = request.POST.get("dataInicio")
        dataFim = request.POST.get("dataFim")
        descricao = request.POST.get("descricao")



        if isDateMaior(dataInicio,dataFim):

            messages.add_message(request,messages.ERROR,"A data fornecida é inválida!")
            return redirect("/configuracoes/relatorio")

            

        novaDisciplina = DisciplinaModel()
        novaDisciplina.nome = nome
        novaDisciplina.data_inicio = dataInicio
        novaDisciplina.data_termino = dataFim
        novaDisciplina.descricao = descricao

        try:

            novaDisciplina.save()
            messages.add_message(request, messages.SUCCESS, 'Disciplina cadastrada com sucesso')


        except IntegrityError:

            messages.add_message(request, messages.ERROR, 'Já existe uma disciplina cadastrada com este nome')
            
        except Error:

            messages.add_message(request, messages.ERROR, 'Ocorreu algum erro')
            

        return redirect("/configuracoes/relatorio")

def editarDisciplina(request):

    id = request.POST.get("id")
    nome = request.POST.get("nome")
    dataInicio = request.POST.get("dataInicio")
    dataFim = request.POST.get("dataFim")
    descricao = request.POST.get("descricao")
    
    if isDateMaior(dataInicio,dataFim):

        messages.add_message(request,messages.ERROR,"A data fornecida é inválida!")
        return redirect("/configuracoes/relatorio")


    disciplina = get_object_or_404(DisciplinaModel,id=id)



    disciplina.nome = nome
    disciplina.data_inicio = dataInicio
    disciplina.data_termino = dataFim
    disciplina.descricao = descricao

    try:

        disciplina.save()

    except IntegrityError:

        messages.add_message(request, messages.ERROR, 'Já existe uma disciplina cadastrada com este nome')
        
    except Error:

        messages.add_message(request, messages.ERROR, 'Ocorreu algum erro')

    return redirect("/configuracoes/relatorio")
 


def deletarDisciplina(request):

    if(request.method == "POST"):

        id = request.POST.get("id")
        disciplina = get_object_or_404(DisciplinaModel,id=id)

        nome = disciplina.nome

        try:
            disciplina.delete()
            messages.add_message(request,messages.SUCCESS,f"A disciplina {nome} foi excluida com sucesso!")

        except ValueError:

            messages.add_message(request,messages.ERROR,"Não foi possivel deletar a disciplina")

    return redirect("/configuracoes/relatorio")


def uploadAssinatura(request):
 
    if(request.method == "POST"):

    
        imagem_base64 = request.POST.get("imagem_base64")
        url = request.POST.get("urlOrigem")
        imagem = Image.open(io.BytesIO(base64.b64decode(imagem_base64)))
        output = io.BytesIO()
        imagem.save(output, format='png', quality=85)
        output.seek(0)
        arquivo = InMemoryUploadedFile(output, 'ImageField',
                                    "assinatura.png",
                                    'image/png',
                                    sys.getsizeof(output), None)
    
        if(not arquivo):

            messages.add_message(request,messages.WARNING,"É necessário um arquivo")

        assinatura = AssinaturaModel(url_assinatura = arquivo)

        try:

            assinatura.save()
            messages.add_message(request,messages.SUCCESS,"Assinatura salva com sucesso")


        except Exception:

            messages.add_message(request,messages.ERROR,"Ocorreu um error ao salva o arquivo")


    return redirect(url)


def api(request):

    return JsonResponse({"message":"Ola mundo"})