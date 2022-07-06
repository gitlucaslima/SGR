from django.views.generic import TemplateView

# Create your views here.

# class NomedaPaginaView(TemplateView):
#     template_name = 'paginas/NomedaPagina.html'

class CodInicioView(TemplateView):
    template_name = 'paginas/Coordenador/Inicio.html' #Pagina de coord inicial
class CodAvisosView(TemplateView):
    template_name = 'paginas/Coordenador/Avisos.html' #Pagina de coord criar avisos
class CodPrazosView(TemplateView):
    template_name = 'paginas/Coordenador/Prazos.html' #Pagina de coord editar datas de envios

class ModeloView(TemplateView):
    template_name = 'paginas/modelo.html' 
