"""Users app mixins"""

from django.conf import settings

import requests


class ReCaptchaV3Mixin:
    def get_context_data(self, **kwargs):
        """Puts Google Site Key into context"""
        context = super().get_context_data(**kwargs)
        if 'RECAPTCHA_SITE_KEY' not in context:
            context['RECAPTCHA_SITE_KEY'] = settings.RECAPTCHA_SITE_KEY
        return context

    def form_valid(self, form):
        """Checks recaptcha"""
        data = {
            'response': self.request.POST.get('g-recaptcha-response'),
            'secret': settings.RECAPTCHA_SECRET_KEY,
        }
        res = requests.post(
            url='https://www.google.com/recaptcha/api/siteverify',
            data=data
        )

        human = res.json().get('success')

        if human:
            return super().form_valid(form)
        else:
            form.add_error(
                field='__all__',
                error=f'No se pudo verificar el ReCAPTCHA'
            )
            return self.form_invalid(form)
