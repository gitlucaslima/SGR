from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')
    else:
        return redirect('login')

