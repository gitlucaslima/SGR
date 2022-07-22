from django.shortcuts import render

# Controllers do aluno


def alunoHome(request):

    return render(request, "aluno/home.html")


def alunoRelatorio(request):

    return render(request, "aluno/gerarRelatorio.html")


# Controller do tutor
def tutorHome(request):

    return render(request, "tutor/home.html")

# Controller do coordenador


def coordenadorHome(request):

    return render(request, "coordenador/home.html")


# Controller do configuraçoes

def configuracoes(request):

    return render(request, "configuracoes/configuracoesCoordenador.html")


# Controller do avisos

def avisos(request):

    return render(request, "avisos/avisosAluno.html")
