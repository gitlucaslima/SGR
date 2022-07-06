from django.views.generic import TemplateView

# Create your views here.

# class NomedaPaginaView(TemplateView):
#     template_name = 'paginas/NomedaPagina.html'

class IndexView(TemplateView):
    template_name = 'paginas/Coordenador/CoordenadorInicio.html' #Pagina de visitantes(usuario deslogado)

class ModeloView(TemplateView):
    template_name = 'paginas/modelo.html' #Pagina de visitantes(usuario deslogado)
