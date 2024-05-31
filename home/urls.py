
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login,name="home"),
    path('project', views.project, name='project'),
    path('team', views.team, name='team'),
    path('analysis', views.analysis, name='analysis'),
    path('login', views.login,name="login"),
    path('logout', views.logout,name="logout"),
    path('details', views.details,name="details"),
    path('saveStage', views.saveStage,name="saveStage"),
    path('saveMsg', views.saveMsg,name="saveMsg"),
]
