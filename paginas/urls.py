from django.urls import path

from .views import IndexView, VisitaView

urlpatterns = [
    # path('endereço', MinhaView.as_view(), name='nome-da-url')
    path('', IndexView.as_view(), name='inicio'),
    path('visita/', VisitaView.as_view(), name='visita'),

]
