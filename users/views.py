from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse


# Page d'enregistrement
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Stocker les champs dans la session pour les réutiliser si nécessaire
        request.session['username'] = username
        request.session['password'] = password

        # Vérifier si les mots de passe sont identiques
        if password == password2:
            # Vérifier si le nom d'utilisateur existe déjà
            if User.objects.filter(username=username).exists():
                messages.error(request, "Ce nom d'utilisateur est déjà pris")
                request.session.flush()  # Réinitialiser les champs après l'erreur
            else:
                # Créer un nouvel utilisateur si tout est valide
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "Utilisateur créé avec succès")
                request.session.flush()  # Réinitialiser les champs après la création
                return redirect('login')
        else:
            # Les mots de passe ne correspondent pas
            messages.error(request, "Les mots de passe ne correspondent pas")
            request.session.flush()  # Réinitialiser les champs après l'erreur
    else:
        # Si la méthode n'est pas POST, nettoyer les sessions pour éviter de garder des données d'une ancienne tentative
        request.session.flush()

    return render(request, 'users/register.html')
# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         password2 = request.POST['password2']

#         if password == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, "Ce nom d'utilisateur est déjà pris")
#             else:
#                 user = User.objects.create_user(username=username, password=password)
#                 user.save()
#                 messages.success(request, "Utilisateur créé avec succès")
#                 return redirect('login')
#         else:
#             messages.error(request, "Les mots de passe ne correspondent pas")
#     return render(request, 'users/register.html')

# Page de connexion

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Essayer de s'authentifier avec les données fournies
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Si l'authentification réussie, connecter l'utilisateur
            login(request, user)
            return redirect('home')
        else:
            # Vérifier si l'utilisateur existe
            if not User.objects.filter(username=username).exists():
                messages.error(request, "Nom d'utilisateur incorrect")
            else:
                messages.error(request, "Mot de passe incorrect")
    
    return render(request, 'users/login.html')

# Page d'accueil après connexion
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users/home.html', {'username': request.user.username})

# Déconnexion
def logout_view(request):
    logout(request)
    return redirect('login')