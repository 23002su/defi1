from django.shortcuts import render, redirect, get_object_or_404
from .forms import GroupeForm, MatiereForm, FiliereForm, EnseignantForm
from .models import Matiere, Groupe, Charge, Affectation, Disponibilite, Chevauchement, Enseignant
from django.http import JsonResponse
from ortools.linear_solver import pywraplp
import openpyxl
import pandas as pd
import os
from django.conf import settings
from django.contrib import messages
from .ortools_model import ScheduleSolver
# Define paths


def home(request):
    """
    Renders the main layout page (base.html).
    """
    return render(request, 'base.html')


def liste_groupes(request):
    groupes = Groupe.objects.all()
    return render(request, 'groupes/liste_groupes.html', {'groupes': groupes})

def creer_groupe(request):
    if request.method == 'POST':
        form = GroupeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_groupes')
    else:
        form = GroupeForm()
    return render(request, 'groupes/groupe_form.html', {'form': form})

def modifier_groupe(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    if request.method == 'POST':
        form = GroupeForm(request.POST, instance=groupe)
        if form.is_valid():
            form.save()
            return redirect('liste_groupes')
    else:
        form = GroupeForm(instance=groupe)
    return render(request, 'groupes/groupe_form.html', {'form': form})

def supprimer_groupe(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    if request.method == 'POST':
        groupe.delete()
        return redirect('liste_groupes')
    return render(request, 'groupes/groupe_confirm_delete.html', {'groupe': groupe})


def liste_matieres(request):
    matieres = Matiere.objects.all()
    return render(request, 'matieres/liste_matieres.html', {'matieres': matieres})

def creer_matiere(request):
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_matieres')
    else:
        form = MatiereForm()
    return render(request, 'matieres/matiere_form.html', {'form': form})

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
def supprimer_matiere(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == 'POST':
        matiere.delete()
        return redirect('liste_matieres')
    return render(request, 'matieres/matiere_confirm_delete.html', {'matiere': matiere})


def liste_filieres(request):
    filieres = Filiere.objects.all()
    return render(request, 'filieres/liste_filieres.html', {'filieres': filieres})

def creer_filiere(request):
    if request.method == 'POST':
        form = FiliereForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_filieres')
    else:
        form = FiliereForm()
    return render(request, 'filieres/filiere_form.html', {'form': form})

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

def supprimer_filiere(request, pk):
    filiere = get_object_or_404(Filiere, pk=pk)
    if request.method == 'POST':
        filiere.delete()
        return redirect('liste_filieres')
    return render(request, 'filieres/filiere_confirm_delete.html', {'filiere': filiere})


def liste_enseignants(request):
    enseignants = Enseignant.objects.all()
    return render(request, 'enseignants/liste_enseignants.html', {'enseignants': enseignants})

def creer_enseignant(request):
    if request.method == 'POST':
        form = EnseignantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_enseignants')
    else:
        form = EnseignantForm()
    return render(request, 'enseignants/enseignant_form.html', {'form': form})

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

def supprimer_enseignant(request, pk):
    enseignant = get_object_or_404(Enseignant, pk=pk)
    if request.method == 'POST':
        enseignant.delete()
        return redirect('liste_enseignants')
    return render(request, 'enseignants/enseignant_confirm_delete.html', {'enseignant': enseignant})


def schedule_view(request):
    if request.method == 'GET':
        data_file = os.path.join(settings.BASE_DIR, 'scheduler', 'data', 'Données.xlsx')
        solver = ScheduleSolver(data_file)
        solver.load_data()
        if solver.solve():
            return JsonResponse({'status': 'success', 'message': 'Schedule generated successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No solution found.'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)