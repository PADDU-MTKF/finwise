
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
    path('cache', views.clear_cache,name="cache"),
    
    path('saveStage', views.saveStage,name="saveStage"),
    path('saveMsg', views.saveMsg,name="saveMsg"),
    path('saveCurrentStage', views.saveCurrentStage,name="saveCurrentStage"),
    path('saveCurrentWorkers', views.saveCurrentWorkers,name="saveCurrentWorkers"),
    path('updateProDet', views.updateProDet,name="updateProDet"),
    path('updateStageDetails', views.updateStageDetails,name="updateStageDetails"),
    path('deleteStage', views.deleteStage,name="deleteStage"),
    path('saveComplete', views.saveComplete,name="saveComplete"),
    path('deleteProject', views.deleteProject,name="deleteProject"),
]
