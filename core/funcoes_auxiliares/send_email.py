
from django.core.mail import EmailMultiAlternatives
from core.models import AvisoModel
from sgr.settings import EMAIL_HOST_USER
from django.utils import timezone


def enviar_email(assunto: str, body_email: str, remetente, destinatarios: list) -> bool:

    try:
        aviso = AvisoModel()
        aviso.assunto = assunto
        aviso.conteudo = body_email
        aviso.tipo_aviso = 1
        aviso.usuario_remetente = remetente
        aviso.data_envio = timezone.now()
        aviso.save()

        to = []
        for usuario in destinatarios:
            aviso.aluno.add(usuario)
            to.append(usuario.email)
            aviso.save()

        from_email = EMAIL_HOST_USER
        text_content = 'This is an important message.'
        msg = EmailMultiAlternatives(assunto, text_content, from_email, to)
        msg.attach_alternative(body_email, "text/html")
        
        try:
            msg.send()
            return True

        except Exception as e:
            aviso.delete()
       
            return False


    except Exception as e2:
       
        return False         
   