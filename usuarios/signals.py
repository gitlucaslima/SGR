from django.db.models.signals import post_save
from django.dispatch import receiver
from rolepermissions.roles import assign_role

from .models import Users


@receiver(post_save, sender=Users)
def define_permissoes(sender, instance, created, **kwargs):
    if created:
        if instance.funcao == "C":
            assign_role(instance, 'coordenador')
        elif instance.funcao == "T":
            assign_role(instance, 'tutor')
        elif instance.funcao == "A":
            assign_role(instance, 'aluno')
