from django.shortcuts import render, redirect, get_object_or_404
from .forms import GroupeForm
from .models import Groupe

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