# ml_trainr URL Configuration

from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),

]

urlpatterns += [

    path('upload/', views.upload, name='upload'),

]
