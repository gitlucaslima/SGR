from django.urls import path

from . import views

urlpatterns = [
    path('cadastrar_tutor/', views.cadastrar_tutor, name="cadastrar_tutor"),
    path('login/', views.login, name="login"),  
    path('sair/', views.logout, name="sair") 
]
