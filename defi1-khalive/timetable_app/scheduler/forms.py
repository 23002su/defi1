from django import forms
from .models import Groupe, Matiere, Filiere, Enseignant

# Formulaire pour le modèle Filiere
class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = ['nom']

# Formulaire pour le modèle Matiere
class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['code', 'nom', 'credits', 'semestre', 'filiere']
        widgets = {
            'filiere': forms.Select(attrs={'class': 'form-control'}),  # Personnalisation de l'élément 'filiere' avec une classe CSS
        }

# Formulaire pour le modèle Groupe
class GroupeForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = ['nom', 'semestre', 'matieres']

# Formulaire pour le modèle Enseignant
class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['nom', 'enseignant_id']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de l\'enseignant'}),
            'enseignant_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'ID de l\'enseignant'}),
        }