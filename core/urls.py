
from django.urls import path

from core.views import *

urlpatterns = [

    path("",login,name="login"),

    path("logout/",logout,name="logout"),
    
    path("aluno/home/", alunoHome, name="aluno_home"),

    path("aluno/gerar_relatorio/", alunoRelatorio, name="aluno_relatorio"),

    path("tutor/home/", tutorHome, name="tutor_home"),

    path("coordenador/home/", coordenadorHome, name="coordenador_home"),

    path("configuracoes/<str:relatorio>", configuracoes, name="configuracoes"),

    path("avisos/", avisos, name="avisos"),

    path("enviar_avisos/",enviarAvisos,name="enviar_avisos"),

    path("registro/", registro, name="registro"),

    path("redefinicao_senha/<str:token>/<int:id>", redefine_senha, name="redefine_senha"),

    path("nova_senha/",nova_senha,name="nova_senha"),

    path("cadastro_usuario/", cadastroUsuario, name="cadastro_usuario"),

    path("edita_usuario/<int:id>/", editaUsuario, name="edita_usuario"),

    path("deleta_usuario/", deletaUsuario, name="deleta_usuario"),

    path("cadastrar_disciplina/", cadastrarDisciplina,
         name="cadastrar_disciplina"),

    path("editar_disciplina/", editarDisciplina, name="editar_disciplina"),

    path("deletar_disciplina/", deletarDisciplina, name="deletar_disciplina"),

    path("apload_assinatura/", uploadAssinatura, name="apload_assinatura"),

    path("abrir_relatorio/", cadastrarRelatorio, name='abrir_relatorio'),

    path("editar_relatorio/", editaRelatorio, name='editar_relatorio'),

    path("deletar_relatorio/", deletarRelatorio, name='deletar_relatorio'),

    path("salvar_atividade/", salvarAtividades, name="salvar_atividade"),

    path("editar_relatorio/<int:id>",editarAtividade,name="editar_relatorio"),

    path("update_relatorio/",update_relatorio,name="update_relatorio"),

    path("excluir_documento/",excluirDocumento,name="excluir_documento")

]
