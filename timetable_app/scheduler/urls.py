from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('groupes/', views.liste_groupes, name='liste_groupes'),
    path('groupes/creer/', views.creer_groupe, name='creer_groupe'),
    path('groupes/modifier/<int:pk>/', views.modifier_groupe, name='modifier_groupe'),
    path('groupes/supprimer/<int:pk>/', views.supprimer_groupe, name='supprimer_groupe'),
]