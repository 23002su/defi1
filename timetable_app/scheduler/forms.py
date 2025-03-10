from django import forms
from .models import Groupe, Matiere, Filiere,Enseignant

class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = ['nom']

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['code', 'nom', 'credits', 'semestre', 'filiere']
        widgets = {
            'filiere': forms.Select(attrs={'class': 'form-control'}),
        }

class GroupeForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = ['nom', 'semestre', 'matieres']
        
class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['nom', 'enseignant_id']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de l\'enseignant'}),
            'enseignant_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'ID de l\'enseignant'}),
        }   
        
class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['nom', 'enseignant_id']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de l\'enseignant'}),
            'enseignant_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'ID de l\'enseignant'}),
        }   
        
                