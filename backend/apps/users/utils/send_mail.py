from django.conf import settings
from django.core.mail import send_mail


def send_reset_password_mail(user, token):
    domain = settings.FRONTEND_DOMAIN
    change_url = f'{domain}/#/zmiana-hasla/{token}'
    send_mail(
        subject=f'Zmiana hasła w systemie Voltra dla loginu: {user.username}',
        message=f'Skopiuj i wklej w przeglądarkę link do zmiany hasła: {change_url}',
        from_email='przypomnieniehasla@system.voltra.pl',
        recipient_list=[user.email],
        fail_silently=True,
    )
