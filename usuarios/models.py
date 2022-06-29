from random import choices

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Users(AbstractUser):
    choices_funcao=(('C','Coordenador'),
                    ('T','Tutor'),
                    ('A','Aluno'),
    )
    funcao = models.CharField(max_length=1, choices=choices_funcao)
