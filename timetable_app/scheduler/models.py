from django.db import models

class Matiere(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Code de la matière (ex: MATH101)
    nom = models.CharField(max_length=100)               # Nom de la matière (ex: Mathématiques)
    credits = models.IntegerField()                      # Nombre de crédits
    semestre = models.IntegerField()                     # Semestre (1, 2, 3, 4, 5, 6)
    filiere = models.CharField(max_length=10)            # Filière (TC, DWM, DSI, RSS)

    def __str__(self):
        return f"{self.code} - {self.nom}"


class Enseignant(models.Model):
    nom = models.CharField(max_length=100)              # Nom de l'enseignant
    enseignant_id = models.CharField(max_length=10, unique=True)  # ID de l'enseignant

    def __str__(self):
        return self.nom


class Groupe(models.Model):
    nom = models.CharField(max_length=10, unique=True)  # Nom du groupe (ex: G1, TP1)
    semestre = models.IntegerField()                    # Semestre (1, 2, 3, 4, 5, 6)
    matieres = models.ManyToManyField(Matiere)          # Matières assignées au groupe

    def __str__(self):
        return self.nom


class Disponibilite(models.Model):
    JOUR_CHOICES = [
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
    ]

    CRENEAU_CHOICES = [
        (1, '8h-9h30'),
        (2, '9h45-11h15'),
        (3, '11h30-13h'),
        (4, '15h-16h30'),
        (5, '16h45-18h15'),
    ]

    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)  # Enseignant
    jour = models.CharField(max_length=10, choices=JOUR_CHOICES)         # Jour de la semaine
    creneau = models.IntegerField(choices=CRENEAU_CHOICES)               # Créneau horaire
    est_disponible = models.BooleanField(default=True)                   # Statut de disponibilité

    class Meta:
        unique_together = ('enseignant', 'jour', 'creneau')  # Éviter les doublons

    def __str__(self):
        return f"{self.enseignant} - {self.jour} - {self.get_creneau_display()}"


class CreneauEmploiDuTemps(models.Model):
    TYPE_CHOICES = [
        ('CM', 'Cours Magistral (CM)'),
        ('TD', 'Travaux Dirigés (TD)'),
        ('TP', 'Travaux Pratiques (TP)'),
    ]

    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)      # Groupe
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)    # Matière
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)  # Enseignant
    jour = models.CharField(max_length=10, choices=Disponibilite.JOUR_CHOICES)  # Jour de la semaine
    creneau = models.IntegerField(choices=Disponibilite.CRENEAU_CHOICES)  # Créneau horaire
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)       # Type de séance (CM, TD, TP)

    class Meta:
        unique_together = ('groupe', 'jour', 'creneau')  # Éviter les chevauchements de créneaux pour un groupe

    def __str__(self):
        return f"{self.groupe} - {self.matiere} - {self.get_type_display()} - {self.jour} - {self.get_creneau_display()}"