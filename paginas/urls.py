from django.urls import path

from .views import CodAvisosView, CodInicioView, CodPrazosView, ModeloView

urlpatterns = [
    # Paginas Coordenador
    path('coordenador/Avisos/', CodAvisosView.as_view(), name='codavisos'),
    path('coordenador/Inicio/', CodInicioView.as_view(), name='codinicio'),
    path('coordenador/Prazos/', CodPrazosView.as_view(), name='codprazos'),

    path('modelo/', ModeloView.as_view(), name='modelo'),

    # path('visita/', VisitaView.as_view(), name='visita'),
    # path('endereço', MinhaView.as_view(), name='nome-da-url')

]
