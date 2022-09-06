

from django.contrib.auth.models import User
from django.db import models

# Variaveis globais
STATUS_CHOICE = (

    (1, "ativo"),
    (2, "desativado")
)

PERMISSAO_CHOICE = (

    (1, "aluno"),
    (2, "tutor"),
    (3, "coordenador")
)


# Model de assinatura
class AssinaturaModel(models.Model):

    url_assinatura = models.ImageField(upload_to="uploads/assinatura/")


# Model de usuario
class UsuarioModel(User):

    global STATUS_CHOICE
    global PERMISSAO_CHOICE


    permissao = models.IntegerField(
        choices=PERMISSAO_CHOICE
    )    

# Admin modelcls



class AdminModel(UsuarioModel):

    ...

# Model do coordenador


class CoordenadorModel(AdminModel):

    class Meta:

        abstract = False


class TutorModel(AdminModel):

    global PERMISSAO_CHOICE

    assinatura = models.OneToOneField(
        AssinaturaModel,
        on_delete=models.SET_NULL,
        null=True,
    )


# Model do aluno
class AlunoModel(UsuarioModel):

    global PERMISSAO_CHOICE

    assinatura = models.OneToOneField(
        AssinaturaModel,
        on_delete=models.SET_NULL,
        null=True,
    )


# Model disciplina

class DisciplinaModel(models.Model):

    STATUS_DISCIPLINA_CHOISE = (

        (1, "Ativa"),
        (2, "Inativa")
    )
    nome = models.CharField(

        max_length=200,
        null=False,
        blank=False,
        unique=True
    )

    descricao = models.TextField(

        max_length=400,
        null=True,
        blank=True
    )

    data_inicio = models.DateField(

        null=False,
        blank=False
    )

    data_termino = models.DateField(
        null=False,
        blank=False
    )

    status = models.IntegerField(

        choices=STATUS_DISCIPLINA_CHOISE,
        default=1,
        null=False
    )

# Model Relatório


class RelatorioModel(models.Model):

    MESES_CHOICE = (

        (1, "Janeiro"),
        (2, "Fevereiro"),
        (3, "Março"),
        (4, "Abril"),
        (5, "Maio"),
        (6, "Junho"),
        (7, "Julho"),
        (8, "Agosto"),
        (9, "Setembro"),
        (10, "Outubro"),
        (11, "Novembro"),
        (12, "Dezembro"),
    )

    STATUS_CHOICE = (

        (1, "aberto"),
        (2, "fechado")
    )

    data_relatorio = models.DateField(

        unique=True,
        null=False,
        blank=False
    )

    data_limite = models.DateField(

        null=False,
        blank=False
    )

    status = models.IntegerField(

        choices=STATUS_CHOICE,
        null=False,
        default=1
    )

    usuario = models.ForeignKey(

        AdminModel,
        null=True,
        on_delete=models.SET_NULL
    )

    disciplina = models.ManyToManyField(DisciplinaModel)


# Model Documento


class DocumentModel(models.Model):

    relatorio = models.ForeignKey(

        RelatorioModel,
        on_delete=models.CASCADE,
        null=False
   
    )

    aluno = models.ForeignKey(

        AlunoModel,
        on_delete=models.CASCADE,
        null=False
    )

    tutor = models.ForeignKey(

        TutorModel,
        null=True,
        on_delete=models.SET_NULL
    )

    url_documento = models.FileField(upload_to="relatorios/")

    conteudo = models.TextField(

        null=False,
        blank=False
    )

    disciplina = models.ManyToManyField(

        DisciplinaModel,
        related_name='relatar_disciplina'
    )

# Model email administrativo da plataforma

# class RelatoModel(models.Model):

#     conteudo = models.TextField

class EmailAdministrativo(models.Model):

    STATUS_CHOISE = (

        (1, "Email_Administrativo"),
    )

    email = models.EmailField(
        null=False,
        blank=False,
        unique=True
    ),

    status = models.IntegerField(

        choices=STATUS_CHOISE,
        unique=True,
        default=1
    )


# Models aviso

class AvisoModel(models.Model):

    email_origem = models.OneToOneField(
        EmailAdministrativo,
        on_delete=models.SET_NULL,
        null=True
    )

    usuario_remetente = models.ForeignKey(

        AdminModel,
        on_delete=models.SET_NULL,
        null=True
    )

    aluno = models.ManyToManyField(

        AlunoModel
    )

    conteudo = models.TextField(

        null=False
    )
