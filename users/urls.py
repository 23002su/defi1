from django.urls import path
from . import views
from django.shortcuts import redirect

 
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('enseignant_home/', views.enseignant_home, name='enseignant_home'),
    path('etudiant_home/', views.etudiant_home, name='etudiant_home'),
   
]