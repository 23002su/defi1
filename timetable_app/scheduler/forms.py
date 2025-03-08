from django import forms
from .models import Groupe

class GroupeForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = ['nom', 'semestre', 'matieres']