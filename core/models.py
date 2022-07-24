
from abc import abstractclassmethod
from pyexpat import model
from xml.etree.ElementInclude import default_loader
from django.db import models


# Model de assinatura
class AssinaturaModel(models.Model):

    url_assinatura = models.CharField(

        max_length=200,
        null= False,
        blank=False
    ) 


# Model de usuario 
class UsuarioModel(models.Model):

    STATUS_CHOICE = (

        (1,"ativo"),
        (2,"desativado")
    )

    nome = models.CharField(

        max_length=200,
        null= False,
        blank= False
    )

    email = models.EmailField(

        null= False,
        blank= False,
        unique= True
    )

    senha = models.CharField(
        null=False,
        blank=False,
        max_length=6
    )

    status = models.IntegerField(

        null=False,
        blank=False,
        choices=STATUS_CHOICE,
        default=2 
    )

    class Meta:

        abstract = True


# Model de admin
class AdminModel(UsuarioModel):

    ...

# Model do coordenador
class CoordenadorModel(AdminModel):

    class Meta:

        abstract = True

class TutorModel(AdminModel):

    assinatura = models.OneToOneField(
        AssinaturaModel,
        on_delete= models.SET_NULL,
        null=True,
    )

# Model do aluno
class AlunoModel(UsuarioModel):

    assinatura = models.OneToOneField(
        AssinaturaModel,
        on_delete= models.SET_NULL,
        null=True,
    )


# Model Relatório
class RelatorioModel(models.Model):

    MESES_CHOICE = (

        (1,"Janeiro"),
        (2,"Fevereiro"),
        (3,"Março"),
        (4,"Abril"),
        (5,"Maio"),
        (6,"Junho"),
        (7,"Julho"),
        (8,"Agosto"),
        (9,"Setembro"),
        (10,"Outubro"),
        (11,"Novembro"),
        (12,"Dezembro"),
    )

    STATUS_CHOICE = (

        (1,"aberto"),
        (2,"fechado")
    )

    mes = models.IntegerField(

        choices= MESES_CHOICE,
        null= False,
        blank= False,
    
    )

    data_limite = models.DateField(

        null= False,
        blank=False
    )

    status = models.IntegerField(

        choices=STATUS_CHOICE,
        null=False,
        default=2
    )

    usuario = models.ForeignKey(

        AdminModel,
        null=True,
        on_delete=models.SET_NULL
    )


# Model disciplina

class DisciplinaModel(models.Model):

    nome = models.CharField(

        max_length=200,
        null= False,
        blank=False,
    )

    descricao = models.TextField(

        max_length=400,
        null=True,
        blank=True
    )

    relatorio = models.OneToOneField(

        RelatorioModel,
        on_delete=models.SET_NULL,
        null=True,
    )

    data_inicio = models.DateField(

        null=False,
        blank=False
    )

    data_termino = models.DateField(
        null=False,
        blank=False
    )

# Model Documento

class DocumentModel(models.Model):

    relatorio = models.OneToOneField(

        RelatorioModel,
        on_delete= models.CASCADE,
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

    url_documento = models.CharField(

        max_length=200,
        null=False,
        blank=False
    )


# Model Relato
class RelatoModel(models.Model):

    documento = models.ForeignKey(

        DocumentModel,
        on_delete=models.SET_NULL,
        null=True
    )

    aluno = models.ForeignKey(

        AlunoModel,
        null=False,
        on_delete=models.CASCADE
    )

    disciplina = models.OneToOneField(

        DisciplinaModel,
        on_delete=models.CASCADE,
        null=False
    )

    conteudo = models.TextField(
        null=False,
        blank=True
    )


# Model email administrativo da plataforma
class EmailAdministrativo(models.Model):

    STATUS_CHOISE = (

        (1,"Email_Administrativo"),
    )

    email = models.EmailField(
        null=False,
        blank=False,
        unique=True
    ),

    status = models.IntegerField(

        choices=STATUS_CHOISE,
        unique=True,
        default= 1
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