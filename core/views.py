"""Core app views"""

from django.shortcuts import render


def handler404(request):
    """Renders a custom 500 page"""
    render(request, '404.html')


def handler500(request):
    """Renders  a custom 500 page"""
    render(request, '500.html')
