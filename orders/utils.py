"""Utilitary functions for orders"""

import os

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.templatetags.static import static


token_generator = PasswordResetTokenGenerator()
STATIC_ROOT = os.path.join(settings.BASE_DIR, 'static')


def ask_for_rating(order, request):
    """Sends an email asking user for rate a order"""
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'
    domain = protocol + request.get_host()

    subject = "[Turing's Food] Califica tu pedido"
    logo_url = domain + static('img/Eating.png')
    html_message = render_to_string(
        template_name='orders/rating-email.html',
        context={
            'domain': domain,
            'logo_url': logo_url,
            'order_id': order.id
        }
    )
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [order.user.email, ]
    msg = EmailMessage(subject, html_message, email_from, recipient_list)
    msg.content_subtype = "html"
    regular_font = os.path.join(STATIC_ROOT, 'fonts/SourceSansPro-Regular.ttf')
    bold_font = os.path.join(STATIC_ROOT, 'fonts/SourceSansPro-Bold.ttf')
    msg.attach_file(regular_font)
    msg.attach_file(bold_font)
    msg.send()
