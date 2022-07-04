from django.views.generic import TemplateView

# Create your views here.

# class NomedaPaginaView(TemplateView):
#     template_name = 'paginas/NomedaPagina.html'

class IndexView(TemplateView):
    template_name = 'paginas/visita.html' #Pagina de visitantes(usuario deslogado)

