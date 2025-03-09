from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from .models import CustomUser
import random
import string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required



def generate_random_password(length=8):
    """Génère un mot de passe aléatoire de longueur donnée."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Une fois le mot de passe changé, mettre à jour le champ `is_password_temp` à False
            request.user.is_password_temp = False
            request.user.save()

            messages.success(request, 'Votre mot de passe a été changé avec succès.')
            return redirect('login')  # Redirige vers la page de connexion après un changement réussi
        else:
            messages.error(request, 'Erreur dans le changement de mot de passe.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'users/change_password.html', {'form': form})
 
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        category = request.POST['category']  # Récupère la catégorie

        if category == 'enseignant' or category == 'etudiant':
            # Vérifie si l'utilisateur existe déjà
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request, "Cet utilisateur existe déjà, vous pouvez vous connecter.")
                return redirect('login')
            else:
                # Si l'utilisateur n'existe pas, crée un mot de passe généré aléatoirement
                password = generate_random_password()
                user = CustomUser.objects.create_user(username=username, password=password, category=category)
                user.save()

                # Envoi d'un message pour informer l'admin ou l'utilisateur de son mot de passe temporaire
                messages.success(request, f"Utilisateur créé avec succès. Votre mot de passe temporaire est : {password}")
                return redirect('login')

        else:
            # Cas où la catégorie n'est ni 'enseignant' ni 'etudiant'
            messages.error(request, "La catégorie choisie n'est pas valide")
    
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Tente d'authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Stocker la catégorie et le nom d'utilisateur dans la session
            request.session['category'] = user.category
            request.session['user'] = user.username

            # Vérifiez si l'utilisateur utilise un mot de passe temporaire
            if user.category in ['enseignant', 'etudiant']:
                # Remplacer 'motdepasse_temporaire' par la logique de votre mot de passe temporaire
                if user.is_password_temp:  # Mot de passe temporaire
                    messages.info(request, "Votre mot de passe est temporaire. Pensez à le changer.")
                    return redirect('change_password')  # Rediriger vers une page pour changer le mot de passe

            # Redirection selon la catégorie de l'utilisateur
            if user.category == 'admin':
                return redirect('admin_home')
            elif user.category == 'enseignant':
                return redirect('enseignant_home')
            else:
                return redirect('etudiant_home')

        else:
            # Si l'authentification échoue
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    # Passer la session dans le contexte
    return render(request, 'users/login.html', {'category': request.session.get('category')})
 
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