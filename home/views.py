"""
Home App - Views
---------------------
Views for home app

"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.shortcuts import render
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def home(request):
    """
    Renders the index template as the home page.
    """
    return render(request, 'index.html')


def custom_404_view(request, *args, **kwargs):
    """
    Custom 404 view.
    """
    response = render(request, '404.html', status=404)
    return response


def custom_403_view(request, *args, **kwargs):
    """
    Custom 403 view.
    """
    response = render(request, '403.html', status=403)
    return response


def custom_500_view(request, *args, **kwargs):
    """
    Custom 404 view.
    """
    response = render(request, '500.html', status=500)
    return response
