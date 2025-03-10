from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        category = request.POST['category']  # Récupère la catégorie

        if password == password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Ce nom d'utilisateur est déjà pris")
            else:
                # Créer un utilisateur avec le modèle personnalisé
                user = CustomUser.objects.create_user(username=username, password=password, category=category)
                user.save()

                messages.success(request, "Utilisateur créé avec succès")
                return redirect('login')
        else:
            messages.error(request, "Les mots de passe ne correspondent pas")

    return render(request, 'users/register.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Stocker la catégorie et le nom d'utilisateur dans la session
            request.session['category'] = user.category  # Catégorie de l'utilisateur
            request.session['user'] = user.username  # Nom d'utilisateur

            # Redirection selon la catégorie de l'utilisateur
            if user.category == 'admin':
                return redirect('admin_home')
            elif user.category == 'enseignant':
                return redirect('enseignant_home')
            else:
                return redirect('etudiant_home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'users/login.html')

# Page d'accueil après connexion
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Récupérer les valeurs de la session
    category = request.session.get('category', 'etudiant')  # Par défaut 'etudiant'
    user = request.session.get('user', request.user.username)  # Par défaut le nom de l'utilisateur connecté
    
    if category == 'admin':
        return render(request, 'users/admin_home.html', {'username': user, 'category': category})
    elif category == 'enseignant':
        return render(request, 'users/enseignant_home.html', {'username': user, 'category': category})
    else:
        return render(request, 'users/etudiant_home.html', {'username': user, 'category': category})

# Déconnexion
def logout_view(request):
    logout(request)
    request.session.flush()  # Réinitialiser la session
    return redirect('login')
# Page d'accueil pour les admin
def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users/admin_home.html', {'username': request.user.username})

# Page d'accueil pour les enseignants
def enseignant_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users/enseignant_home.html', {'username': request.user.username})

# Page d'accueil pour les étudiants
def etudiant_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users/etudiant_home.html', {'username': request.user.username})