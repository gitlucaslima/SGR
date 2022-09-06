import base64

import io
import sys
from asyncio.windows_events import NULL
from datetime import datetime

from msilib.schema import Error
from xmlrpc.client import DateTime

from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from PIL import Image

from core.funcoes_auxiliares.data import isDateMaior
from core.models import *
from django.contrib.auth.decorators import login_required,user_passes_test
from docxtpl import DocxTemplate
from sgr.settings import EMAIL_HOST_USER,ALLOWED_HOSTS
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator    
from django.contrib.auth import login as login_check
from django.contrib.auth import logout as logout_django
from django.core.signing import Signer
from django.core.signing import TimestampSigner

# Controllers do aluno

# Controller do login

def login(request):

    if request.method == "GET":

        return render(request, 'partius/gerenciarAcesso/login.html')

    email = request.POST.get('email')
    senha = request.POST.get("senha")

    usuario = UsuarioModel.objects.get(email=email)

    
    is_equal_password = usuario.check_password(senha)

    if(is_equal_password):
        
        login_check(request, usuario)

        request.session['permissao'] = usuario.permissao

        if usuario.permissao == 1:
            return redirect("/aluno/home/")    
        elif usuario.permissao == 2:
            return redirect("/tutor/home/")    
        else:
            return redirect("/coordenador/home/")    


def logout(request):

    logout_django(request)

    return redirect("login")


@login_required(login_url="login")
def alunoHome(request):

    relatorios = RelatorioModel.objects.all().order_by("-data_relatorio")

    context = {

        "url": "aluno_home",
        "relatorios":relatorios

    }
    return render(request, "aluno/home.html", context)


def alunoRelatorio(request):

    relatorio_abertos = RelatorioModel.objects.filter(
        status=1).order_by("-data_relatorio")

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
    relatorios = RelatorioModel.objects.all().order_by("-data_relatorio")
    ultimoRelatorio = relatorios[0] if relatorios else NULL

    contexto = {
        "tab": dados,
        "numeroAlunos": dados.count(),
        "relatorios": relatorios,
        "ultimoRelatorio": ultimoRelatorio
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

    relatorios = RelatorioModel.objects.all().order_by("data_relatorio")

    anoAtual = datetime.now().year
    mesAtual = datetime.now().month

    ultimoRelatorio = RelatorioModel.objects.all().order_by("-data_relatorio")

    # Obtem o mês do ultimo relatório realizado no ano virgente, caso não exista nenhum relatório relizado nessas circuntâcias retorna o mês atual do ano virgente
    ultimoRelatorio = int(ultimoRelatorio[0].data_relatorio.month) if ultimoRelatorio and int(
        ultimoRelatorio[0].data_relatorio.year) == anoAtual else mesAtual-1
    ultimoRelatorioRealizado = ultimoRelatorio

    # Obtem o proximo ano do relatorio de acordo com o ultimo relatorio
    anoAtual = int(anoAtual)+1 if ultimoRelatorio == 12 else anoAtual
    # Obtem o proximo mes do relatorio
    ultimoRelatorio = 1 if ultimoRelatorio == 12 else ultimoRelatorio+1

    ultimoRelatorioFormat = ultimoRelatorio if ultimoRelatorio >= 10 else '0' + \
        str(ultimoRelatorio)
    contexto = {
        "tab": relatorio,
        "disciplinas": disciplinas,
        "listDisciplinas": listDisciplinas,
        "relatorios": relatorios,
        "ultimoRelatorio": ultimoRelatorio,
        "ultimoRelatorioFormat": ultimoRelatorioFormat,
        "anoAtual": anoAtual,
        "mesAtual": mesAtual,
        "meses": MESES_CHOICE,
        "ultimoRelatorioRealizado": ultimoRelatorioRealizado
    }

    if relatorio == 'usuario':

        dados = UsuarioModel.objects.all()

        contexto['dados_usuarios'] = dados

    return render(request, "configuracoes/configuracoes.html", contexto)


# Controller do avisos

def avisos(request):

    return render(request, "aluno/avisosAluno.html")

# Controller do registro

def registro(request):

    return render(request, 'partius/gerenciarAcesso/registro.html')


# Controller do registro

def redefine_senha(request,token,id):

    if request.method == "GET":

        usuario = get_object_or_404(User,id=id)
        is_usuario = default_token_generator.check_token(usuario, token)

        if(is_usuario):

            return render(request, 'partius/gerenciarAcesso/redefinicaoSenha.html',{"usuario":usuario})

        else:
             
            return redirect('/login/')

def nova_senha(request):

    if request.method == "POST":

        id = request.POST.get("id")
        senha = request.POST.get("senha")
        senha_repeat = request.POST.get("senha_repeat")

        usuario = get_object_or_404(User,id=id)

        if senha == senha_repeat:

            usuario.set_password(senha)
            usuario.save()
            messages.add_message(request,messages.SUCCESS,"Senha alterada com sucesso")

        else:

            messages.add_message(request,messages.ERROR,"As senha precisão ser iguais")

    return redirect("login")

# Cadastro de usuarios


def cadastroUsuario(request):

    if request.method == "POST":

        nome = request.POST.get("nome")
        email = request.POST.get("email")
        permissao = request.POST.get("permissao")

        if(permissao == '1'):

            novo_usuario = AlunoModel()
            novo_usuario.username = nome
            novo_usuario.email = email
            novo_usuario.permissao = 1
            novo_usuario.is_active = False

        elif permissao == '2':
            novo_usuario = TutorModel()
            novo_usuario.username = nome
            novo_usuario.email = email
            novo_usuario.permissao = 2
            novo_usuario.is_active = False
            novo_usuario.is_superuser = True
            novo_usuario.is_staff = True

        else:
            novo_usuario = CoordenadorModel()
            novo_usuario.username = nome
            novo_usuario.email = email
            novo_usuario.permissao = 3
            novo_usuario.is_active = True
            novo_usuario.is_superuser = True
            novo_usuario.is_staff = True

        try:

            novo_usuario.save()

            try:

                token = default_token_generator.make_token(novo_usuario)

                dados = {

                    "url_redefinir":f"{request.headers['Origin']}/redefinicao_senha/{token}/{novo_usuario.id}"
                }

                body_email = render_to_string("emailTemplate/confirmacaoSenha.html",dados)
        
                assunto = "Confirmação de usuário"
                from_email =  EMAIL_HOST_USER 
                to = novo_usuario.email
                text_content = 'This is an important message.'
                msg = EmailMultiAlternatives(assunto, text_content, from_email, [to])
                msg.attach_alternative(body_email, "text/html")
                msg.send()

                messages.add_message(request,messages.SUCCESS,"Usuário foi criado com sucesso. Um email foi enviado para o email fornecido.")
            
            except Exception as e:
                print(e)
                messages.add_message(request,messages.ERROR,"Email não pode ser enviado")
                return redirect("/configuracoes/usuario")
                
               
        except Exception as e1:

            messages.add_message(request,messages.ERROR,"Ocorreu algum erro ao criar o usuário")
            return redirect("/configuracoes/usuario")

    return redirect("/configuracoes/usuario")


def editaUsuario(request, id):

    if request.method == "POST":

        instance = UsuarioModel.objects.filter(id=id).first()

        instance.username = request.POST.get("nome")
        instance.email = request.POST.get("email")
        instance.permissao = request.POST.get("permissao")
        instance.is_active = request.POST.get("status")
      

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

        messages.add_message(request, messages.SUCCESS,
                             "Alterações realizadas com sucesso!")
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
        
        aluno = get_object_or_404(AlunoModel,id=request.user.id)

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
            aluno.assinatura = assinatura
            aluno.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Assinatura salva com sucesso")

        except Exception:

            messages.add_message(request, messages.ERROR,
                                 "Ocorreu um error ao salvar o arquivo")

    return redirect(url)


def cadastrarRelatorio(request):

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
    if request.method == "POST":

        mes = request.POST.get('mesRelatorio')
        dataLimite = request.POST.get('dataLimite')
        disciplinas = request.POST.getlist('disciplina')
        status = request.POST.get("status")

        relatorios_abertos = RelatorioModel.objects.filter(status=1)

        if(relatorios_abertos and status == '1'):

            messages.add_message(request, messages.WARNING,
                                 "Já existe um relatório aberto. Relatório mês - {0}".format(MESES_CHOICE[int(relatorios_abertos[0].data_relatorio.month-1)][1]))

            return redirect('/configuracoes/relatorio')
        ano_atual = anoAtual = datetime.now().year

        # Pegando o mês da data limite

        if(dataLimite):
            mes_dataLimite = int(dataLimite.split('-')[1])

        else:
            messages.add_message(request, messages.ERROR,
                                 "É necessário fornecer uma data limite para entrega do relatório")

            return redirect('/configuracoes/relatorio')
        ano_limite = int(dataLimite.split('-')[0])

        if(mes_dataLimite < int(mes) and ano_limite < int(anoAtual)):

            messages.add_message(request, messages.ERROR,
                                 "Data limite é anterior ao mês do relatório")

            return redirect('/configuracoes/relatorio')

        if(not disciplinas):

            messages.add_message(request, messages.ERROR,
                                 "É necessário fornecer uma disciplina ou mais")

            return redirect('/configuracoes/relatorio')

        mes = mes if int(mes) >= 10 else '0'+str(mes)

        relatorio = RelatorioModel()
        relatorio.data_relatorio = "{0}-{1}-01".format(ano_atual, mes)
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

            registro = DisciplinaModel.objects.get(id=int(disciplina_id))
            relatorio.disciplina.add(registro)
            relatorio.save()

    return redirect('/configuracoes/relatorio')


def editaRelatorio(request):

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
    if request.method == "POST":

        id = request.POST.get("id")
        mesRelatorio = request.POST.get("mesRelatorio")
        dataLimite = request.POST.get("dataLimite")
        disciplinas = request.POST.getlist("disciplina")
        status = request.POST.get("status")

        relatorio = get_object_or_404(RelatorioModel, id=id)

        anoAtual = datetime.now().year

        mesRelatorio = mesRelatorio if int(
            mesRelatorio) >= 10 else '0'+mesRelatorio

        nova_data_relatorio = "{0}-{1}-01".format(anoAtual, mesRelatorio)

        # Busca todos os relatórios com a nova data
        relatorio_data = RelatorioModel.objects.filter(
            data_relatorio=nova_data_relatorio)

        # Verifica se existe algum relatório nessa data e se é do relatorio editado
        if relatorio_data and relatorio_data[0].id != int(id):

            messages.add_message(request, messages.ERROR,
                                 "Já existe um relatório nessa data!")

            return redirect("/configuracoes/relatorio")

        relatorios_abertos = RelatorioModel.objects.filter(status=1)

        if(relatorios_abertos and relatorios_abertos[0].id != int(id) and status == '1'):

            messages.add_message(request, messages.WARNING,
                                 "Já existe um relatório aberto. Relatório mês - {0}".format(MESES_CHOICE[int(relatorios_abertos[0].data_relatorio.month-1)][1]))

            return redirect('/configuracoes/relatorio')

        if not disciplinas:

            messages.add_message(request, messages.WARNING,
                                 "No minimo uma disciplina deve ser selecionada")
            return redirect("/configuracoes/relatorio")

        relatorio.data_relatorio = nova_data_relatorio
        relatorio.data_limite = dataLimite
        relatorio.status = status

        relatorio.disciplina.clear()

        for item in disciplinas:

            registro = DisciplinaModel.objects.get(id=int(item))
            relatorio.disciplina.add(registro)
            relatorio.save()

            messages.add_message(request, messages.SUCCESS,
                                 "alterações realizadas com sucesso!")

    return redirect("/configuracoes/relatorio")


def deletarRelatorio(request):
    if (request.method == "POST"):
        id = request.POST.get("id")
        nome = request.POST.get("nome")

        relatorio = get_object_or_404(RelatorioModel, id=id)

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

        mesReferencia = request.POST.get("mesReferencia")
        nomeDisciplina = request.POST.getlist("nomeDisciplina")
        dataInicio = request.POST.getlist("dataInicio")
        dataFim = request.POST.getlist("dataFim")
        atividades = request.POST.getlist("atividades")
        relatorioCorrente = request.POST.get("periodo_relatorio")

        relatorio = get_object_or_404(RelatorioModel,id=relatorioCorrente)
        
        aluno = get_object_or_404(AlunoModel, id=request.user.id)
        assintura_aluno = aluno.assinatura.url_assinatura
          
        # Importação do doc que será usado como template
        doc = DocxTemplate("media/modelo/modeloRelatorio.docx")

        conteudo = []

        for indice in range(len(nomeDisciplina)):
            conteudo.append(
                [nomeDisciplina[indice], dataInicio[indice], dataFim[indice], atividades[indice]])

        # Trocar informações pelas do modelo
        context = {
            "nomeAluno": aluno.username,
            "mesReferencia": mesReferencia,
            "conteudo": conteudo
        }

        # Trocar assinatura do aluno e tutor, pelas do modelo
        doc.replace_pic('Imagem 10', 'media/uploads/assinatura/assinatura.png')
        doc.replace_pic('Imagem 12', assintura_aluno)

        # Aplicar a troca de informações
        doc.render(context)
        # Gerar documento

        # Gerar um hash de
        signer = TimestampSigner()
        value = signer.sign(aluno.email).split(":")[-1]

        # Cria um nome unico para o arquivo
        nome_arquivo = f"media/relatorios/relatorio{value}.docx"
        
        try:


            doc.save(nome_arquivo)

        except Exception as e1:
            
            messages.add_message(request,messages.ERROR,"Não foi possivel gerar o documento")
            return redirect("/aluno/home")

        novo_documento = DocumentModel()
        novo_documento.aluno = aluno
        novo_documento.conteudo = ''
        novo_documento.relatorio = relatorio
        novo_documento.url_documento = nome_arquivo

        try:

            novo_documento.save()

            messages.add_message(request,messages.SUCCESS, "Relatório gerado com sucesso")

        except Exception as e:

            messages.add_message(request,messages.ERROR, "Não foi possivel gerar o documento")


        return redirect("/aluno/home")
