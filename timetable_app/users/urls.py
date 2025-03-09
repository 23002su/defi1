from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('enseignant-home/', views.enseignant_home, name='enseignant_home'),
    path('etudiant-home/', views.etudiant_home, name='etudiant_home'),
    path('home/', views.home, name='home'),
]