

from datetime import date, datetime
from django.contrib.auth.models import User
from django.db import models
from django_unused_media import cleanup
from docxtpl import DocxTemplate
from django.core.signing import TimestampSigner

from core.funcoes_auxiliares.converteData import converteMes

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




# Model de usuario
class UsuarioModel(User):

    global STATUS_CHOICE
    global PERMISSAO_CHOICE


    permissao = models.IntegerField(
        choices=PERMISSAO_CHOICE
    )

    def delete(self,using=None, keep_parents=False):

        cleanup.remove_unused_media()
        super(UsuarioModel,self).delete(using=using,keep_parents=keep_parents)    

# Model de assinatura
class AssinaturaModel(models.Model):

    usuario = models.ForeignKey(UsuarioModel,on_delete=models.CASCADE)
    url_assinatura = models.ImageField(upload_to="uploads/assinatura/")

    def delete(self,using=None, keep_parents=False):

        cleanup.remove_unused_media()
        super(AssinaturaModel,self).delete(using=using,keep_parents=keep_parents)


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

    def delete(self,using=None, keep_parents=False):

        cleanup.remove_unused_media()
        super(DisciplinaModel,self).delete(using=using,keep_parents=keep_parents)

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

        UsuarioModel,
        null=True,
        on_delete=models.SET_NULL
    )

    disciplina = models.ManyToManyField(DisciplinaModel)

    def delete(self,using=None, keep_parents=False):

        cleanup.remove_unused_media()
        super(RelatorioModel,self).delete(using=using,keep_parents=keep_parents)




# Model Documento
class DocumentModel(models.Model):

    relatorio = models.ForeignKey(

        RelatorioModel,
        on_delete=models.CASCADE,
        null=False
   
    )

    aluno = models.ForeignKey(

        UsuarioModel,
        on_delete=models.CASCADE,
        null=False,
        related_name="aluno_autor"
    )

    tutor = models.ForeignKey(

        UsuarioModel,
        null=True,
        on_delete=models.SET_NULL,
        related_name="tutor_responsavel"
    )

    url_documento = models.FileField(upload_to="relatorios/")

 
    disciplina = models.ManyToManyField(

        DisciplinaModel,
        related_name='relatar_disciplina'
    )

    data_update = models.DateField()

    
    def delete(self,using=None, keep_parents=False):

        cleanup.remove_unused_media()
        super(DocumentModel,self).delete(using=using,keep_parents=keep_parents)

    
    def gerarRelatorio(self):

        conteudo = []

        relatos = RelatoModel.objects.filter(documento=self).order_by("id")
        for relato in relatos:

            disciplina = relato.disciplina
            conteudo.append(
                [disciplina.nome, disciplina.data_inicio.strftime("%d/%m/%Y"), disciplina.data_termino.strftime("%d/%m/%Y"), relato.conteudo])
        
    
        conteudo = {
            "nomeAluno": self.aluno.username,
            "mesReferencia":  converteMes(self.relatorio.data_relatorio.month),
            "conteudo": conteudo
        }


        doc = DocxTemplate("static/modelo/modeloRelatorio.docx")

        doc.render(conteudo)
  
        return doc  

    def salvarRelatorio(self,doc: DocxTemplate):
        
        # Exclui arquivo anterios da pasta
        cleanup.remove_unused_media()

        signer = TimestampSigner()
        value = signer.sign(self.aluno.email).split(":")[-1]
        
        # Cria um nome unico para o arquivo
        nome_arquivo = f"media/uploads/relatorios/relatorio{self.aluno.username}{value}.docx"
      
        
        doc.save(nome_arquivo)

        # atualiza documento com o novo arquivo
        self.url_documento = nome_arquivo

        self.save()



    def assinarDocumento(self):

        doc = self.gerarRelatorio()
        
        # Verifica se aluno e/ou tutor para assinar documento
        if self.aluno:
            assinatura = AssinaturaModel.objects.get(usuario=self.aluno)
            doc.replace_pic('Imagem 12', assinatura.url_assinatura)

        if self.tutor:
            assinatura = AssinaturaModel.objects.get(usuario=self.tutor)
            doc.replace_pic('Imagem 10',assinatura.url_assinatura)            

     
        self.salvarRelatorio(doc)

class RelatoModel(models.Model):

    documento = models.ForeignKey(DocumentModel,on_delete=models.CASCADE)
    disciplina = models.ForeignKey(DisciplinaModel,on_delete=models.CASCADE)    
    conteudo = models.TextField()

    def delete(self,using=None, keep_parents=False):

        cleanup.remove_unused_media()
        super(RelatoModel,self).delete(using=using,keep_parents=keep_parents)

# Model email administrativo da plataforma
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

    email_origem = models.CharField(null=False,blank=False,max_length=100)

    assunto = models.CharField(null=False,blank=False,max_length=150)

    usuario_remetente = models.ForeignKey(

        UsuarioModel,
        on_delete=models.SET_NULL,
        null=True
    )

    aluno = models.ManyToManyField(

        UsuarioModel,
        related_name="aluno_destinatario"
    )

    conteudo = models.TextField(

        null=False
    )
    
    data_envio = models.DateTimeField()
