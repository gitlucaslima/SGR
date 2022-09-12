
from django.core.mail import EmailMultiAlternatives
from sgr.settings import EMAIL_HOST_USER


def enviar_email(assunto:str,body_email: str, destinatarios: list[str]) -> bool:

    from_email = EMAIL_HOST_USER
    to = destinatarios
    text_content = 'This is an important message.'
    msg = EmailMultiAlternatives(assunto, text_content, from_email, to)
    msg.attach_alternative(body_email, "text/html")

    try:
        msg.send()
        return True

    except Exception as e:

        print(e)
        return False
