
from django.urls import path

from core.views import *

urlpatterns = [

    path("aluno/home/", alunoHome, name="aluno_home"),
    path("aluno/gerar_relatorio/", alunoRelatorio, name="aluno_relatorio"),

    path("tutor/home/", tutorHome, name="tutor_home"),

    path("coordenador/home/", coordenadorHome, name="coordenador_home"),

    path("configuracoes/", configuracoes, name="configuracoes"),

    path("avisos/", avisos, name="avisos"),

    path("login/", login, name="login"),

    path("registro/", registro, name="registro"),

    path("redefinicao_senha/", redefine_senha, name="redefine_senha"),





]
