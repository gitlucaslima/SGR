# seta as permissões de cada pessoa
from rolepermissions.roles import AbstractUserRole


class Coordenador(AbstractUserRole):
    available_permissions = {
        'status_alunos' : True,
        'emitir_avisos' : True,
        'enviar_mensagens' : True,
        'editar_prazo' : True
    }

class Tutor(AbstractUserRole):
    available_permissions = {
        'status_alunos' : True,
        'emitir_avisos' : True,
        'enviar_mensagens' : True,
        'editar_prazo' : True,
    }

