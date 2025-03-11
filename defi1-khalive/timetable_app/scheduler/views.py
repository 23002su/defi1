from django.shortcuts import render, redirect, get_object_or_404
from .forms import GroupeForm, MatiereForm, FiliereForm, EnseignantForm
from .models import Matiere, Groupe, Charge, Affectation, Disponibilite, Chevauchement, Enseignant
from django.http import JsonResponse, FileResponse
from ortools.linear_solver import pywraplp
import os
from django.conf import settings
from django.contrib import messages
import logging
from .ortools_model import ScheduleSolver

# Vue d'erreur
def error_page(request):
    return render(request, 'error_page.html')


# Vue principale (home)
def home(request):
    try:
        return render(request, 'base.html')
    except Exception as e:
        logging.error(f"Erreur dans la vue 'home': {e}", exc_info=True)
        return redirect('error_page')


# Liste des groupes
def liste_groupes(request):
    try:
        groupes = Groupe.objects.all()
        return render(request, 'groupes/liste_groupes.html', {'groupes': groupes})
    except Exception as e:
        logging.error(f"Erreur dans 'liste_groupes': {e}", exc_info=True)
        return redirect('error_page')


# Créer un groupe
def creer_groupe(request):
    try:
        if request.method == 'POST':
            form = GroupeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('liste_groupes')
        else:
            form = GroupeForm()
        return render(request, 'groupes/groupe_form.html', {'form': form})
    except Exception as e:
        logging.error(f"Erreur dans 'creer_groupe': {e}", exc_info=True)
        return redirect('error_page')


# Modifier un groupe
def modifier_groupe(request, pk):
    try:
        groupe = get_object_or_404(Groupe, pk=pk)
        if request.method == 'POST':
            form = GroupeForm(request.POST, instance=groupe)
            if form.is_valid():
                form.save()
                return redirect('liste_groupes')
        else:
            form = GroupeForm(instance=groupe)
        return render(request, 'groupes/groupe_form.html', {'form': form})
    except Exception as e:
        logging.error(f"Erreur dans 'modifier_groupe': {e}", exc_info=True)
        return redirect('error_page')


# Supprimer un groupe
def supprimer_groupe(request, pk):
    try:
        groupe = get_object_or_404(Groupe, pk=pk)
        if request.method == 'POST':
            groupe.delete()
            return redirect('liste_groupes')
        return render(request, 'groupes/groupe_confirm_delete.html', {'groupe': groupe})
    except Exception as e:
        logging.error(f"Erreur dans 'supprimer_groupe': {e}", exc_info=True)
        return redirect('error_page')


# Liste des matières
def liste_matieres(request):
    try:
        matieres = Matiere.objects.all()
        return render(request, 'matieres/liste_matieres.html', {'matieres': matieres})
    except Exception as e:
        logging.error(f"Erreur dans 'liste_matieres': {e}", exc_info=True)
        return redirect('error_page')


# Créer une matière
def creer_matiere(request):
    try:
        if request.method == 'POST':
            form = MatiereForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('liste_matieres')
        else:
            form = MatiereForm()
        return render(request, 'matieres/matiere_form.html', {'form': form})
    except Exception as e:
        logging.error(f"Erreur dans 'creer_matiere': {e}", exc_info=True)
        return redirect('error_page')


# Supprimer une matière
def supprimer_matiere(request, pk):
    try:
        matiere = get_object_or_404(Matiere, pk=pk)
        if request.method == 'POST':
            matiere.delete()
            return redirect('liste_matieres')
        return render(request, 'matieres/matiere_confirm_delete.html', {'matiere': matiere})
    except Exception as e:
        logging.error(f"Erreur dans 'supprimer_matiere': {e}", exc_info=True)
        return redirect('error_page')

def modifier_matiere(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == 'POST':
        form = MatiereForm(request.POST, instance=matiere)
        if form.is_valid():
            form.save()
            return redirect('liste_matieres')
    else:
        form = MatiereForm(instance=matiere)
    return render(request, 'matieres/matiere_form.html', {'form': form})

# Liste des filières
def liste_filieres(request):
    try:
        filieres = Filiere.objects.all()
        return render(request, 'filieres/liste_filieres.html', {'filieres': filieres})
    except Exception as e:
        logging.error(f"Erreur dans 'liste_filieres': {e}", exc_info=True)
        return redirect('error_page')


# Créer une filière
def creer_filiere(request):
    try:
        if request.method == 'POST':
            form = FiliereForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('liste_filieres')
        else:
            form = FiliereForm()
        return render(request, 'filieres/filiere_form.html', {'form': form})
    except Exception as e:
        logging.error(f"Erreur dans 'creer_filiere': {e}", exc_info=True)
        return redirect('error_page')

def modifier_filiere(request, pk):
    filiere = get_object_or_404(Filiere, pk=pk)
    if request.method == 'POST':
        form = FiliereForm(request.POST, instance=filiere)
        if form.is_valid():
            form.save()
            return redirect('liste_filieres')
    else:
        form = FiliereForm(instance=filiere)
    return render(request, 'filieres/filiere_form.html', {'form': form})

# Supprimer une filière
def supprimer_filiere(request, pk):
    try:
        filiere = get_object_or_404(Filiere, pk=pk)
        if request.method == 'POST':
            filiere.delete()
            return redirect('liste_filieres')
        return render(request, 'filieres/filiere_confirm_delete.html', {'filiere': filiere})
    except Exception as e:
        logging.error(f"Erreur dans 'supprimer_filiere': {e}", exc_info=True)
        return redirect('error_page')


# Liste des enseignants
def liste_enseignants(request):
    try:
        enseignants = Enseignant.objects.all()
        return render(request, 'enseignants/liste_enseignants.html', {'enseignants': enseignants})
    except Exception as e:
        logging.error(f"Erreur dans 'liste_enseignants': {e}", exc_info=True)
        return redirect('error_page')


# Créer un enseignant
def creer_enseignant(request):
    try:
        if request.method == 'POST':
            form = EnseignantForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('liste_enseignants')
        else:
            form = EnseignantForm()
        return render(request, 'enseignants/enseignant_form.html', {'form': form})
    except Exception as e:
        logging.error(f"Erreur dans 'creer_enseignant': {e}", exc_info=True)
        return redirect('error_page')

def modifier_enseignant(request, pk):
    enseignant = get_object_or_404(Enseignant, pk=pk)
    if request.method == 'POST':
        form = EnseignantForm(request.POST, instance=enseignant)
        if form.is_valid():
            form.save()
            return redirect('liste_enseignants')
    else:
        form = EnseignantForm(instance=enseignant)
    return render(request, 'enseignants/enseignant_form.html', {'form': form})

# Supprimer un enseignant
def supprimer_enseignant(request, pk):
    try:
        enseignant = get_object_or_404(Enseignant, pk=pk)
        if request.method == 'POST':
            enseignant.delete()
            return redirect('liste_enseignants')
        return render(request, 'enseignants/enseignant_confirm_delete.html', {'enseignant': enseignant})
    except Exception as e:
        logging.error(f"Erreur dans 'supprimer_enseignant': {e}", exc_info=True)
        return redirect('error_page')


# Téléchargement du planning
def download_schedule(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'scheduler', 'data', '1emploi.xlsx')  # Mettez à jour le chemin si nécessaire
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        else:
            return JsonResponse({'status': 'error', 'message': 'File not found.'}, status=404)
    except Exception as e:
        logging.error(f"Erreur dans 'download_schedule': {e}", exc_info=True)
        return redirect('error_page')
    
def schedule_view(request):
    try:
        if request.method == 'GET':
            # Définir le chemin du fichier Excel contenant les données
            data_file = os.path.join(settings.BASE_DIR, 'scheduler', 'data', 'Données.xlsx')

            # Vérifier si le fichier existe avant de tenter de le charger
            if not os.path.exists(data_file):
                return JsonResponse({'status': 'error', 'message': f'File {data_file} not found.'}, status=404)

            # Si le fichier existe, créer une instance de ScheduleSolver
            solver = ScheduleSolver(data_file)
            
            # Charger les données depuis le fichier Excel
            solver.load_data()

            # Résoudre le planning et récupérer les données du planning généré
            if solver.solve():  # Résoudre le problème
                emploi_du_temps = solver.get_schedule()  # Récupérer l'emploi du temps généré

                # Assurez-vous que l'emploi du temps est sous forme de dictionnaire avec des jours comme clés
                if not emploi_du_temps:
                    return JsonResponse({'status': 'error', 'message': 'Aucun emploi du temps généré.'})

                # Vérification de la structure de l'emploi du temps pour chaque jour de la semaine
                days_of_week = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
                emploi_du_temps = {day: emploi_du_temps.get(day, []) for day in days_of_week}
                
                # Retourner le résultat sous forme de rendu de template
                return render(request, 'generated_schedule.html', {
                    'emploi_du_temps': emploi_du_temps, 
                    'message': 'Emploi du temps généré avec succès.'
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Aucune solution trouvée pour l\'emploi du temps.'})
        
        # Si la méthode de la requête n'est pas GET
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    except Exception as e:
        # Gestion des erreurs générales et affichage du message d'erreur dans les logs
        logging.error(f"Error in 'schedule_view': {str(e)}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'}, status=500)
    
