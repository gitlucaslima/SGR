from django.urls import path

from .views import (AluInicioView, CodAvisosView, CodInicioView, CodPrazosView,
                    ModeloView)

urlpatterns = [
    # Paginas Coordenador
    path('coordenador/avisos/', CodAvisosView.as_view(), name='codavisos'),
    path('coordenador/inicio/', CodInicioView.as_view(), name='codinicio'),
    path('coordenador/prazos/', CodPrazosView.as_view(), name='codprazos'),

    # Paginas Aluno
    path('aluno/inicio/', AluInicioView.as_view(), name='aluinicio'),

    path('modelo/', ModeloView.as_view(), name='modelo'),

    # path('visita/', VisitaView.as_view(), name='visita'),
    # path('endereço', MinhaView.as_view(), name='nome-da-url')

]
