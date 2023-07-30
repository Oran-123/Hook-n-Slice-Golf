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


def custom_404_view(request, *args, **argv):
    """
    Custom 404 view.
    """
    response = render_to_response(
        '404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def custom_403_view(request, *args, **argv):
    """
    Custom 403 view.
    """
    response = render_to_response(
        '403.html', {}, context_instance=RequestContext(request))
    response.status_code = 403
    return response


def custom_500_view(request, *args, **argv):
    """
    Custom 404 view.
    """
    response = render_to_response(
        '500.html', {}, context_instance=RequestContext(request))
    response.status_code = 403
    return response
