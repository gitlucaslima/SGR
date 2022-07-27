
from django.urls import path

from core.views import *

urlpatterns = [

    path("aluno/home/", alunoHome, name="aluno_home"),

    path("aluno/gerar_relatorio/", alunoRelatorio, name="aluno_relatorio"),

    path("tutor/home/", tutorHome, name="tutor_home"),

    path("coordenador/home/", coordenadorHome, name="coordenador_home"),

    path("configuracoes/<str:relatorio>", configuracoes, name="configuracoes"),

    path("configuracoes/<str:usuario>", configuracoes, name="configuracoes"),

    path("configuracoes/<str:aviso>", configuracoes, name="configuracoes"),

    path("avisos/", avisos, name="avisos"),

    path("login/", login, name="login"),

    path("registro/", registro, name="registro"),

    path("redefinicao_senha/", redefine_senha, name="redefine_senha"),

    path("cadastro_usuario/",cadastroUsuario, name="cadastro_usuario"),

    path("edita_usuario/<int:id>/", editaUsuario, name="edita_usuario"),

    path("deleta_usuario/<int:id>/", deletaUsuario, name="deleta_usuario"),


]
