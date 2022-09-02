import base64
import io
import sys
from asyncio.windows_events import NULL
from datetime import datetime
from io import BytesIO
from msilib.schema import Error
from sqlite3 import Date
from tkinter import OUTSIDE

from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from PIL import Image

from core.funcoes_auxiliares.data import isDateMaior
from core.models import *

# Controllers do aluno


def alunoHome(request):

    context = {

        "url": "aluno_home"

    }
    return render(request, "aluno/home.html", context)


def alunoRelatorio(request):

    relatorio_abertos = RelatorioModel.objects.filter(
        status=1).order_by("-mes")

    ultimo_relatorio = relatorio_abertos[0] if relatorio_abertos else NULL

    contexto = {

        "relatorio_corrente": ultimo_relatorio
    }
    return render(request, "aluno/gerarRelatorio.html", contexto)


# Controller do tutor
def tutorHome(request):

    context = {

        "url": "tutor_home"

    }
    return render(request, "tutor/home.html", context)


# Controller do coordenador

def coordenadorHome(request):

    dados = UsuarioModel.objects.filter(permissao=1)

    contexto = {
        "tab": dados,
        "numeroAlunos": dados.count()

    }

    contexto['dados_usuarios'] = dados

    return render(request, "coordenador/home.html", contexto)


# Controller do configuraçoes

def configuracoes(request, relatorio):

    MESES_CHOICE = [

        [1, "Janeiro"],
        [2, "Fevereiro"],
        [3, "Março"],
        [4, "Abril"],
        [5, "Maio"],
        [6, "Junho"],
        [7, "Julho"],
        [8, "Agosto"],
        [9, "Setembro"],
        [10, "Outubro"],
        [11, "Novembro"],
        [12, "Dezembro"]
    ]
    disciplinas = DisciplinaModel.objects.filter(status=1)
    listDisciplinas = DisciplinaModel.objects.all()
    # Preparando os dados do relatorio para fornecer os nomes dos meses
    relatorios = [(item, MESES_CHOICE[item.mes-1][1])
                  for item in RelatorioModel.objects.all().order_by("mes")]

    ultimoRelatorio = RelatorioModel.objects.all().order_by(
        "-mes")[0].mes if RelatorioModel.objects.all().order_by("-mes") else NULL
    anoAtual = datetime.now().year
    mesAtual = datetime.now().month

    contexto = {
        "tab": relatorio,
        "disciplinas": disciplinas,
        "listDisciplinas": listDisciplinas,
        "meses": MESES_CHOICE,
        "relatorios": relatorios,
        "ultimoRelatorio": ultimoRelatorio,
        "anoAtual": anoAtual,
        "mesAtual": mesAtual
    }

    if relatorio == 'usuario':

        dados = UsuarioModel.objects.all()

        contexto['dados_usuarios'] = dados

    return render(request, "coordenador/configuracoesCoordenador.html", contexto)


# Controller do avisos

def avisos(request):

    return render(request, "aluno/avisosAluno.html")

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
        instance = get_object_or_404(UsuarioModel, id=id)
        instance.delete()

    return redirect("/configuracoes/usuario")


def cadastrarDisciplina(request):

    if(request.method == "POST"):

        nome = request.POST.get("nome")
        dataInicio = request.POST.get("dataInicio")
        dataFim = request.POST.get("dataFim")
        descricao = request.POST.get("descricao")

        if isDateMaior(dataInicio, dataFim):

            messages.add_message(request, messages.ERROR,
                                 "A data fornecida é inválida!")
            return redirect("/configuracoes/disciplinas")

        novaDisciplina = DisciplinaModel()
        novaDisciplina.nome = nome
        novaDisciplina.data_inicio = dataInicio
        novaDisciplina.data_termino = dataFim
        novaDisciplina.descricao = descricao

        try:

            novaDisciplina.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Disciplina cadastrada com sucesso')

        except IntegrityError:

            messages.add_message(
                request, messages.ERROR, 'Já existe uma disciplina cadastrada com este nome')

        except Error:

            messages.add_message(request, messages.ERROR, 'Ocorreu algum erro')

        return redirect("/configuracoes/disciplinas")


def editarDisciplina(request):

    id = request.POST.get("id")
    nome = request.POST.get("nome")
    dataInicio = request.POST.get("dataInicio")
    dataFim = request.POST.get("dataFim")
    descricao = request.POST.get("descricao")

    if isDateMaior(dataInicio, dataFim):

        messages.add_message(request, messages.ERROR,
                             "A data fornecida é inválida!")
        return redirect("/configuracoes/disciplinas")

    disciplina = get_object_or_404(DisciplinaModel, id=id)

    disciplina.nome = nome
    disciplina.data_inicio = dataInicio
    disciplina.data_termino = dataFim
    disciplina.descricao = descricao

    try:

        disciplina.save()

    except IntegrityError:

        messages.add_message(request, messages.ERROR,
                             'Já existe uma disciplina cadastrada com este nome')

    except Error:

        messages.add_message(request, messages.ERROR, 'Ocorreu algum erro')

    return redirect("/configuracoes/disciplinas")


def deletarDisciplina(request):

    if(request.method == "POST"):

        id = request.POST.get("id")
        disciplina = get_object_or_404(DisciplinaModel, id=id)

        nome = disciplina.nome

        try:
            disciplina.delete()
            messages.add_message(request, messages.SUCCESS,
                                 f"A disciplina {nome} foi excluida com sucesso!")

        except ValueError:

            messages.add_message(request, messages.ERROR,
                                 "Não foi possivel deletar a disciplina")

    return redirect("/configuracoes/disciplinas")


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

            messages.add_message(request, messages.WARNING,
                                 "É necessário um arquivo")

        assinatura = AssinaturaModel(url_assinatura=arquivo)

        try:

            assinatura.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Assinatura salva com sucesso")

        except Exception:

            messages.add_message(request, messages.ERROR,
                                 "Ocorreu um error ao salva o arquivo")

    return redirect(url)


def cadastrarRelatorio(request):

    if request.method == "POST":

        mes = request.POST.get('mesRelatorio')
        dataLimite = request.POST.get('dataLimite')
        disciplinas = request.POST.getlist('disciplina')
        status = request.POST.get("status")

        # Pegando o mês da data limite
        mes_dataLimite = int(dataLimite.split('-')[1])

        if(mes_dataLimite < int(mes)):

            messages.add_message(request, messages.ERROR,
                                 "Data limite é anterior ao mês do relatório")

            return redirect('/configuracoes/relatorio')

        if(not disciplinas):

            messages.add_message(request, messages.ERROR,
                                 "É necessário fornecer uma disciplina ou mais")

            return redirect('/configuracoes/relatorio')

        relatorio = RelatorioModel()
        relatorio.mes = mes
        relatorio.status = status
        relatorio.data_limite = dataLimite

        try:

            relatorio.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Relatórios criado com sucesso")

        except IntegrityError:

            messages.add_message(request, messages.ERROR,
                                 "Já existe relatório para esse mês")

            return redirect('/configuracoes/relatorio')

        for disciplina_id in disciplinas:
            print(disciplinas)
            registro = DisciplinaModel.objects.get(id=int(disciplina_id))
            relatorio.disciplina.add(registro)
            relatorio.save()

    return redirect('/configuracoes/relatorio')


def editaRelatorio(request):

    if request.method == "POST":
        id = request.POST.get("id")
        mesRelatorio = request.POST.get("mesRelatorio")
        dataLimite = request.POST.get("dataLimite")
        disciplinas = request.POST.getlist("disciplina")
        status = request.POST.get("status")

        relatorio = get_object_or_404(RelatorioModel, id=id)

        relatorio.mes = mesRelatorio
        relatorio.data_limite = dataLimite
        relatorio.status = status
        relatorio.disciplina.clear()

        for item in disciplinas:
            print(item)
            registro = DisciplinaModel.objects.get(id=int(item))
            relatorio.disciplina.add(registro)
            relatorio.save()

    return redirect("/configuracoes/relatorio")


def deletarRelatorio(request):
    if (request.method == "POST"):
        id = request.POST.get("id")
        nome = request.POST.get("nome")

        relatorio = get_object_or_404(RelatorioModel, id=id)
        print(nome)

        try:
            relatorio.delete()
            messages.add_message(request, messages.SUCCESS,
                                 f"O relatorio {nome} foi excluido com sucesso!")

        except ValueError:

            messages.add_message(request, messages.ERROR,
                                 "Não foi possivel deletar o relatorio")

    return redirect("/configuracoes/relatorio")


def salvarAtividades(request):

    if(request.method == "POST"):

        atividades = request.POST.getlist("atividades")

        print(atividades)

        return redirect("/aluno/gerar_relatorio")
