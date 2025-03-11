from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('groupes/', views.liste_groupes, name='liste_groupes'),
    path('groupes/creer/', views.creer_groupe, name='creer_groupe'),
    path('groupes/modifier/<int:pk>/', views.modifier_groupe, name='modifier_groupe'),
    path('groupes/supprimer/<int:pk>/', views.supprimer_groupe, name='supprimer_groupe'),
    path('matieres/', views.liste_matieres, name='liste_matieres'),
    path('matieres/creer/', views.creer_matiere, name='creer_matiere'),
    path('matieres/modifier/<int:pk>/', views.modifier_matiere, name='modifier_matiere'),
    path('matieres/supprimer/<int:pk>/', views.supprimer_matiere, name='supprimer_matiere'),
    path('filieres/', views.liste_filieres, name='liste_filieres'),
    path('filieres/creer/', views.creer_filiere, name='creer_filiere'),
    path('filieres/modifier/<int:pk>/', views.modifier_filiere, name='modifier_filiere'),
    path('filieres/supprimer/<int:pk>/', views.supprimer_filiere, name='supprimer_filiere'),
    path('enseignants/', views.liste_enseignants, name='liste_enseignants'),
    path('enseignants/creer/', views.creer_enseignant, name='creer_enseignant'),
    path('enseignants/modifier/<int:pk>/', views.modifier_enseignant, name='modifier_enseignant'),
    path('enseignants/supprimer/<int:pk>/', views.supprimer_enseignant, name='supprimer_enseignant'),
    path('generate-schedule/', views.schedule_view, name='generate_schedule'),
    path('download-schedule/', views.download_schedule, name='download_schedule'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)