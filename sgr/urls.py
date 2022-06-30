from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('auth/', include('usuarios.urls'))   
]
