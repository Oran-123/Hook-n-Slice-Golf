from django.urls import path
from . import views
from django.conf.urls import handler404
from home.views import custom_404_view


urlpatterns = [
    path('', views.home, name='home'),
]

handler404 = custom_404_view
