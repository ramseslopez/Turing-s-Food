"""Core app views"""

from django.shortcuts import render

def handler404(request, exception):
    """Renders a custom 404 page"""
    render(request, '404.html')


def handler500(request):
    """Renders a custom 500 page"""
    render(request, '500.html')
