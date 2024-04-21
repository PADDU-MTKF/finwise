
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('temp', views.temp,name="temp"),
    path('team', views.team_view, name='team_view'),
    path('finance', views.finance_view, name='finance_view'),
    path('work', views.work_view, name='work_view'),
]
