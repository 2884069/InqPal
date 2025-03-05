from django.urls import path
from inqpal import views

app_name = 'inqpal'

urlpatterns = [
    path('', views.index, name='index'),
]