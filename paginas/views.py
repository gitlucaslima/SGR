from django.views.generic import TemplateView

# Create your views here.

# class NomedaPaginaView(TemplateView):
#     template_name = 'paginas/NomedaPagina.html'


class CodInicioView(TemplateView):
    template_name = 'paginas/Coordenador/Inicio.html'  # Pagina de coord inicial


class CodAvisosView(TemplateView):
    template_name = 'paginas/Coordenador/Avisos.html'  # Pagina de coord criar avisos


class CodPrazosView(TemplateView):
    # Pagina de coord editar datas de envios
    template_name = 'paginas/Coordenador/Prazos.html'


class AluInicioView(TemplateView):
    template_name = 'paginas/Aluno/Inicio.html'  # Pagina de aluno inicial


class AluRelatorioView(TemplateView):
    template_name = 'paginas/Aluno/Relatorio.html'  # Pagina de aluno inicial


class ModeloView(TemplateView):
    template_name = 'paginas/modelo.html'


# Tutor
class TutorInicioView(TemplateView):
    template_name = 'paginas/Tutor/Inicio.html'  # Pagina de tutor inicial


class TutorAvisosView(TemplateView):
    template_name = 'paginas/Tutor/Avisos.html'  # Pagina de tutor avisos


class TutorPrazosView(TemplateView):
    template_name = 'paginas/Tutor/Prazos.html'  # Pagina de tutor prazos
