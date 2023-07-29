from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def custom_403_view(request, exception):
    return render(request, '403.html', status=403)
