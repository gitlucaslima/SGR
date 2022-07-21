from django.urls import path

from .views import (AluAvisosView, AluEnvioView, AluRelatorioView,
                    CodAvisosView, CodInicioView, CodPrazosView,
                    ConfiguracoesView, TutorAvisosView, TutorInicioView,
                    TutorPrazosView)

urlpatterns = [
    # Paginas Coordenador
    path('coordenador/inicio/', CodInicioView.as_view(), name='codinicio'),
    path('coordenador/avisos/', CodAvisosView.as_view(), name='codavisos'),


    # Paginas Tutor
    path('tutor/inicio/', TutorInicioView.as_view(), name='tutinicio'),
    path('tutor/avisos/', TutorAvisosView.as_view(), name='tutavisos'),
    path('tutor/prazos/', TutorPrazosView.as_view(), name='tutprazos'),

    # Paginas Aluno
    path('aluno/avisos/', AluAvisosView.as_view(), name='aluavisos'),
    path('aluno/relatorio/', AluRelatorioView.as_view(), name='alurelatorio'),
    path('aluno/envio/', AluEnvioView.as_view(), name='aluenvio'),

    # Pagina configurações
    path('configuracoes/', ConfiguracoesView.as_view(), name='config'),

    # path('visita/', VisitaView.as_view(), name='visita'),
    # path('endereço', MinhaView.as_view(), name='nome-da-url')

]
