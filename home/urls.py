
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login,name="home"),
    path('temp', views.temp,name="temp"),
    path('team', views.team_view, name='team_view'),
    path('finance', views.finance_view, name='finance_view'),
    path('work', views.work_view, name='work_view'),
    path('login', views.login,name="login"),
    path('logout', views.logout,name="logout"),
]
