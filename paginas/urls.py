from django.urls import path

from .views import IndexView, ModeloView

urlpatterns = [
    # path('endereço', MinhaView.as_view(), name='nome-da-url')
    path('', IndexView.as_view(), name='inicio'),
    path('modelo/', ModeloView.as_view(), name='modelo'),

    # path('visita/', VisitaView.as_view(), name='visita'),

]
