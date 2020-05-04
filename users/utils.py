"""Utilitary functions for users"""

import os

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.templatetags.static import static


token_generator = PasswordResetTokenGenerator()
STATIC_ROOT = os.path.join(settings.BASE_DIR, 'static')


def send_email_confirmation(user, request):
    """Sends an email confirmation for new user"""
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'
    domain = protocol + request.get_host()

    subject = "Confirma tu correo para Turing's Food"
    token = token_generator.make_token(user)
    logo_url = domain + static('img/emailSend.png')
    html_message = render_to_string(
        template_name='users/email-confirmation.html',
        context={
            'token': token,
            'domain': domain,
            'logo_url': logo_url,
            'user_id': user.id
        }
    )
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    msg = EmailMessage(subject, html_message, email_from, recipient_list)
    msg.content_subtype = "html"
    regular_font = os.path.join(STATIC_ROOT, 'fonts/SourceSansPro-Regular.ttf')
    bold_font = os.path.join(STATIC_ROOT, 'fonts/SourceSansPro-Bold.ttf')
    msg.attach_file(regular_font)
    msg.attach_file(bold_font)
    msg.send()


def check_token(user, token):
    """Checks if token is valid"""
    return token_generator.check_token(user, token)
