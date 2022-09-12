import base64
import io

import sys
from asyncio.windows_events import NULL
from datetime import datetime
from msilib.schema import Error

from django.contrib import messages
from django.contrib.auth import login as login_check
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from PIL import Image

from core.funcoes_auxiliares.data import isDateMaior, isDatePassou
from core.funcoes_auxiliares.send_email import enviar_email
from core.models import *
from sgr.settings import EMAIL_BACKEND, EMAIL_HOST_USER

# Controllers do aluno

# Controller do login
def login(request):

    
    permissao = request.session.get('permissao')
    if permissao:

        if permissao == 1:

            return redirect("aluno_home")

        elif permissao == 2:
            return redirect("tutor_home")

        elif permissao == 3:

            return redirect("coordenador_home")

    # Verifca se existe algum usuário
    is_usuarios = len(UsuarioModel.objects.all())

    if(not is_usuarios):


        return redirect('registro')

    if request.method == "GET":

        return render(request, 'partius/gerenciarAcesso/login.html')

    email = request.POST.get('email')
    senha = request.POST.get("senha")

    usuario =  UsuarioModel.objects.filter(email=email).first()
    
    if(not usuario):

        messages.add_message(request,messages.ERROR,"Login ou senha inválidos")
        return redirect("login")


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
    else:

        messages.add_message(request, messages.ERROR,
                             "Login ou senha inválidos")
        return redirect("login")


def logout(request):


    logout_django(request)

    return redirect("login")


@login_required(login_url="login")
def alunoHome(request):

    if request.session['permissao'] != 1:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")

    aluno = get_object_or_404(UsuarioModel,id=request.user.id)
    assinatura = AssinaturaModel.objects.filter(usuario=aluno).first()
    
    documentos = DocumentModel.objects.filter(aluno=aluno).order_by('-id')

    context = {

        "url": "aluno_home",
        "documentos": documentos,
        "assinatura":assinatura

    }
    return render(request, "aluno/home.html", context)


@login_required(login_url="login")
def alunoRelatorio(request):

    if request.session['permissao'] != 1:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")

    relatorio_aberto = RelatorioModel.objects.filter(
        status=1).order_by("-data_relatorio").first()

    if not relatorio_aberto:

        messages.add_message(request,messages.WARNING,"Não existe nenhum relatório disponível")
        return redirect('aluno_home')
    
    if isDatePassou(relatorio_aberto.data_limite):

        messages.add_message(request,messages.WARNING,"Período para entrega do relatório já passou!")
        return redirect('aluno_home')



    aluno = UsuarioModel.objects.get(id=request.user.id)
    relatorio_realizado = list(filter(lambda item: item.aluno == aluno,DocumentModel.objects.filter(relatorio=relatorio_aberto)))
    assinatura = AssinaturaModel.objects.filter(usuario = aluno)

    if not assinatura:
        messages.add_message(request,messages.WARNING,"Forneça uma assinatura.")
        return redirect("/aluno/home")

    if(relatorio_realizado):
        
        messages.add_message(request,messages.WARNING,"Já foi realizado um relatório, edite ou exclua")
        return redirect("/aluno/home")


    contexto = {

        "relatorio_corrente": relatorio_aberto
    }
    return render(request, "aluno/gerarRelatorio.html", contexto)


@login_required(login_url="login")
def tutorHome(request):

    if request.session['permissao'] != 2:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")

    tutor = get_object_or_404(UsuarioModel,id=request.user.id)
    assinatura = AssinaturaModel.objects.filter(usuario=tutor).first()


    context = {

        "url": "tutor_home",
        "assinatura":assinatura

    }
    return render(request, "tutor/home.html", context)


# Controller do coordenador

@login_required(login_url="login")
def coordenadorHome(request):

    if request.session['permissao'] != 3:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")

    dados = UsuarioModel.objects.filter(permissao=1)

    relatorios = [(relatorio,DocumentModel.objects.filter(relatorio=relatorio)) for relatorio in RelatorioModel.objects.all().order_by("-data_relatorio")]

   
    relatoriosEnviados = len(relatorios[0][1] if relatorios else [])
    ultimoRelatorio = relatorios[0][0] if relatorios else NULL
    numAlunos = dados.count()
    relatoriosPendentes = numAlunos - relatoriosEnviados
    
    contexto = {
        "tab": dados,
        "numeroAlunos": numAlunos,
        "relatorios": relatorios,
        "ultimoRelatorio": ultimoRelatorio,
        "relatoriosPendentes":relatoriosPendentes,
        "relatoriosEnviados": relatoriosEnviados
    }

    contexto['dados_usuarios'] = dados

    return render(request, "coordenador/home.html", contexto)


# Controller do configuraçoes

@login_required(login_url="login")
def configuracoes(request, relatorio):

    if request.session['permissao'] == 1:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")

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

@login_required(login_url="login")
def avisos(request):

    if request.session.get('permissao') == 1:
        
        aluno = get_object_or_404(UsuarioModel,id = request.user.id)
        avisos = AvisoModel.objects.filter(aluno=aluno).order_by("-data_envio")
         
        context = {

            'avisos':avisos
        }
        return render(request, "avisos/avisosAluno.html",context)
    
    else:

        avisos = AvisoModel.objects.all().order_by("-data_envio")

        context = {

            'avisos':avisos
        }
        return render(request, "avisos/avisosAdmin.html",context)


# Controller do registro


def registro(request):

    is_usuarios = len(UsuarioModel.objects.all())

    # Impede que alguém acesse essa funcionalidade sem a necessidade
    if is_usuarios:

        return redirect('login')
    if(request.method=="POST"):

        usuario = request.POST.get("usuario")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        senhaRepeat = request.POST.get("senha-repeat")

        if senha == senhaRepeat:

            novo_usuario = UsuarioModel()
            novo_usuario.email= email
            novo_usuario.username = usuario
            novo_usuario.set_password(senha)
            novo_usuario.permissao = 3

            try:

                novo_usuario.save()
                messages.add_message(request,messages.SUCCESS,"Usuário criado com sucesso")
                return redirect('login')                
            except Exception as e:

                messages.add_message(request,messages.ERROR,"Ocorreu um erro ao salvar o usuário, tente mais tarde")
                return redirect("login")

        else:

            messages.add_message(request,messages.ERROR,"A senha não são iguais")
            return redirect("registro")

    else:
        
        return render(request, 'partius/gerenciarAcesso/registro.html')


# Controller do registro

def redefine_senha(request, token, id):

    if request.method == "GET":

        usuario = get_object_or_404(User, id=id)
        is_usuario = default_token_generator.check_token(usuario, token)

        if(is_usuario):

            return render(request, 'partius/gerenciarAcesso/redefinicaoSenha.html', {"usuario": usuario})

        else:

            return redirect('login')


def nova_senha(request):

    if request.method == "POST":

        id = request.POST.get("id")
        senha = request.POST.get("senha")
        senha_repeat = request.POST.get("senha_repeat")

        usuario = get_object_or_404(User, id=id)

        if senha == senha_repeat:

            usuario.set_password(senha)
            usuario.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Senha alterada com sucesso")

        else:

            messages.add_message(request, messages.ERROR,
                                 "As senha precisão ser iguais")

    return redirect("login")

# Cadastro de usuarios

@login_required(login_url="login")
def cadastroUsuario(request):

    if request.session['permissao'] == 1:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")

    if request.method == "POST":

        nome = request.POST.get("nome")
        email = request.POST.get("email")
        permissao = request.POST.get("permissao")

        if(permissao == '1'):

            novo_usuario = UsuarioModel()
            novo_usuario.username = nome
            novo_usuario.email = email
            novo_usuario.permissao = 1
            novo_usuario.is_active = False

        elif permissao == '2':
            novo_usuario = UsuarioModel
            novo_usuario.username = nome
            novo_usuario.email = email
            novo_usuario.permissao = 2
            novo_usuario.is_active = False
            novo_usuario.is_superuser = True
            novo_usuario.is_staff = True

        else:
            novo_usuario = UsuarioModel()
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

                    "url_redefinir": f"{request.headers['Origin']}/redefinicao_senha/{token}/{novo_usuario.id}",
                    "assunto":"Definição de senha",
                    
                }

                body_email = render_to_string(
                    "emailTemplate/confirmacaoSenha.html", dados)

                enviar_email("Confirmação de usuário",body_email,[novo_usuario.email])

                messages.add_message(request,messages.SUCCESS,"Usuário foi criado com sucesso. Um email foi enviado para o email fornecido.")
            
            except Exception as e:
                
                messages.add_message(request,messages.ERROR,"Email não pode ser enviado")
                return redirect("/configuracoes/usuario")
                
               
        except Exception as e1:

            messages.add_message(request,messages.ERROR,"Ocorreu algum erro ao criar o usuário")
            return redirect("/configuracoes/usuario")

    return redirect("/configuracoes/usuario")


@login_required(login_url="login")
def editaUsuario(request, id):

    if request.session['permissao'] == 1:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")

    if request.method == "POST":

        instance = UsuarioModel.objects.filter(id=id).first()

        instance.username = request.POST.get("nome")
        instance.email = request.POST.get("email")
        instance.permissao = request.POST.get("permissao")
        instance.is_active = request.POST.get("status")
      

        instance.save()

    return redirect("/configuracoes/usuario")

@login_required(login_url="login")
def deletaUsuario(request):

    if request.session['permissao'] == 1:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")

    if request.method == 'POST':

        id = request.POST.get('id')
        instance = get_object_or_404(UsuarioModel, id=id)
        instance.delete()

    return redirect("/configuracoes/usuario")


@login_required(login_url='login')
def cadastrarDisciplina(request):

    if request.session['permissao'] == 1:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")

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


@login_required(login_url='login')
def editarDisciplina(request):

    if request.session['permissao'] == 1:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")


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


@login_required(login_url="login")
def deletarDisciplina(request):

    if request.session['permissao'] == 1:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")


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

@login_required(login_url="login")
def uploadAssinatura(request):

    if request.session['permissao'] == 3:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")


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
        
        usuario = get_object_or_404(UsuarioModel,id=request.user.id)
        assinatura = AssinaturaModel.objects.filter(usuario=usuario)
        # Analiza se o aluno possui uma assinatura
        if(assinatura):
           
            # Remove o arquivo anterios se existir
        
            assinatura.delete()
            

        if(not arquivo):

            messages.add_message(request, messages.WARNING,
                                 "É necessário um arquivo")

        assinatura = AssinaturaModel(usuario=usuario,url_assinatura=arquivo)

        try:
            
            assinatura.save()
            messages.add_message(request, messages.SUCCESS,
                                "Assinatura salva com sucesso")

        
        except Exception:

            messages.add_message(request, messages.ERROR,
                                 "Ocorreu um error ao salvar o arquivo")

    return redirect(url)

@login_required(login_url='login')
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

@login_required(login_url="login")
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


@login_required(login_url="login")
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


@login_required(login_url='login')
def salvarAtividades(request):


    if(request.method == "POST"):

        disciplinas_id = request.POST.getlist("nomeDisciplina")
        dataInicio = request.POST.getlist("dataInicio")
        dataFim = request.POST.getlist("dataFim")
        atividades = request.POST.getlist("atividades")
        relatorioCorrente = request.POST.get("periodo_relatorio")

        relatorio = get_object_or_404(RelatorioModel,id=relatorioCorrente)
        aluno = get_object_or_404(UsuarioModel, id=request.user.id)
        relatorio_realizado = list(filter(lambda item: item.aluno == aluno,DocumentModel.objects.filter(relatorio=relatorio)))
        
        if( relatorio_realizado ):
            
            messages.add_message(request,messages.WARNING,"Já foi realizado um relatório, edite ou exclua")
            return redirect("/aluno/home")
       
        conteudo = []

        for indice in range(len(disciplinas_id)):
            nome_disciplina=DisciplinaModel.objects.get(id=disciplinas_id[indice]).nome
            conteudo.append(
                [nome_disciplina, dataInicio[indice], dataFim[indice], atividades[indice]])
            
        novo_documento = DocumentModel()
        novo_documento.aluno = aluno
        novo_documento.relatorio = relatorio
        novo_documento.data_update = datetime.now()

        try:

            novo_documento.save()


            for indice in range(len(atividades)):

                relato_registro = RelatoModel()
                relato_registro.documento = novo_documento
                relato_registro.conteudo = atividades[indice]
                relato_registro.disciplina = DisciplinaModel.objects.get(id=disciplinas_id[indice])
                relato_registro.save()

            messages.add_message(request,messages.SUCCESS, "Relatório gerado com sucesso")
            
            novo_documento.assinarDocumento()

        except Exception as e:
       
            messages.add_message(request,messages.ERROR, "Não foi possivel gerar o documento")


        return redirect("/aluno/home")


@login_required(login_url='login')
def editarAtividade(request,id):

    if request.session['permissao'] != 1:

        messages.add_message(request,messages.INFO,"Usuário não têm acesso a esse recurso")
        return redirect("login")

    if request.method == 'GET':

        documento = get_object_or_404(DocumentModel,id=id)
        relatos = RelatoModel.objects.filter(documento=documento)

        context = {

            "documento": documento,
            "relatos":relatos
        }
       
    return render(request,'aluno/editarRelatorio.html',context)


@login_required(login_url='login')
def update_relatorio(request):

    if(request.method == "POST"):

        documento_id = request.POST.get("id_documento")
        atividades = request.POST.getlist("atividades")
        relato_ids = request.POST.getlist("id_relato")

        documento = get_object_or_404(DocumentModel,id=documento_id)

        for indice,id_relato in enumerate(relato_ids):

            relato = RelatoModel.objects.get(id=id_relato)
            relato.conteudo = atividades[indice]

            relato.save()

        try:
            documento.assinarDocumento()
            messages.add_message(request,messages.SUCCESS,"Documento alterado com sucesso!")

        except Exception:

            messages.add_message(request,messages.ERROR,"Documento não pode ser alterado")

        return redirect("aluno_home")


@login_required(login_url='login')
def excluirDocumento(request):

    
    if request.method == 'POST':
        
        id = request.POST.get('id')
        documento = get_object_or_404(DocumentModel,id=id)

        try:
            
            documento.delete()
            messages.add_message(request,messages.SUCCESS,"Documento deletado com sucesso!")

        except Exception:

            messages.add_message(request,messages.ERROR,"Documento não pode ser deletado")


    return redirect('aluno_home')


# Controle de avisos

@login_required(login_url="login")
def enviarAvisos(request):

    usuario = get_object_or_404(UsuarioModel,id=request.user.id)

    if request.method == 'POST':

        destinatario = int(request.POST.get('destinatario'))
        assunto = request.POST.get('assunto')
        conteudo = request.POST.get('conteudo')

        # EMAIL_HOST_USER

        if destinatario == -1:

            destinatarios = UsuarioModel.objects.filter(permissao=1)

        emails = []

        if not emails:

            messages.add_message(request,messages.WARNING,"Nenhum aluno foi encontrado. Cadastre primeiramente algum aluno")
            return redirect('avisos')



        for aluno in destinatarios:

            emails.append(aluno.email)

    
        enviado = enviar_email(assunto=assunto,body_email=conteudo,destinatarios=emails)

        if enviado:

            aviso = AvisoModel()
            aviso.conteudo =conteudo
            aviso.email_origem = EMAIL_HOST_USER
            aviso.usuario_remetente = usuario
            aviso.assunto = assunto
            aviso.data_envio = datetime.now()
            aviso.save()

            for aluno in destinatarios:

                aviso.aluno.add(aluno)
                aviso.save()
            
            messages.add_message(request,messages.SUCCESS,"Aviso enviado com sucesso!")

        else:

            messages.add_message(request,messages.ERROR,"Ocorreu um erro ao enviar o aviso!")


     
    return redirect('avisos')

   

