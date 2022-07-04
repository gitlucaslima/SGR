from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = 'paginas/visitante.html'

class VisitaView(TemplateView):
    template_name = 'paginas/modelo.html'
