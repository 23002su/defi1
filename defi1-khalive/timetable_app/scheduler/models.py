from django.db import models


class Filiere(models.Model):
    nom = models.CharField(max_length=50, unique=True)  # Nom de la filière (ex: TC, DWM, DSI, RSS)

    def __str__(self):
        return self.nom


class Matiere(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Code de la matière (ex: MATH101)
    nom = models.CharField(max_length=100)               # Nom de la matière (ex: Mathématiques)
    credits = models.IntegerField()                      # Nombre de crédits
    semestre = models.IntegerField()                     # Semestre (1, 2, 3, 4, 5, 6)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='matieres')  # Relation avec Filiere

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


class Charge(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)  # Matière
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)    # Groupe
    cm = models.IntegerField(default=0)                            # Charge CM
    tp = models.IntegerField(default=0)                            # Charge TP
    td = models.IntegerField(default=0)                            # Charge TD

    class Meta:
        unique_together = ('matiere', 'groupe')  # Éviter les doublons

    def __str__(self):
        return f"{self.matiere} - {self.groupe} (CM: {self.cm}, TP: {self.tp}, TD: {self.td})"


class Affectation(models.Model):
    TYPE_CHOICES = [
        ('CM', 'Cours Magistral (CM)'),
        ('TP', 'Travaux Dirigés (TP)'),
        ('TD', 'Travaux Pratiques (TD)'),
    ]

    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)  # Matière
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)    # Groupe
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)  # Enseignant
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)    # Type de séance (CM, TP, TD)

    class Meta:
        unique_together = ('matiere', 'groupe', 'type')  # Éviter les doublons

    def __str__(self):
        return f"{self.matiere} - {self.groupe} - {self.get_type_display()} - {self.enseignant}"


class Chevauchement(models.Model):
    groupe1 = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='chevauchements_groupe1')  # Groupe 1
    groupe2 = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='chevauchements_groupe2')  # Groupe 2
    chevauchement = models.BooleanField(default=False)  # Chevauchement autorisé ou non

    class Meta:
        unique_together = ('groupe1', 'groupe2')  # Éviter les doublons

    def __str__(self):
        return f"{self.groupe1} - {self.groupe2} - Chevauchement: {self.chevauchement}"


class GestionDisponibilite:
    def __init__(self, enseignant):
        self.enseignant = enseignant

    def ajouter_disponibilite(self, jour, creneau, est_disponible=True):
        """Ajoute ou modifie la disponibilité d'un enseignant pour un créneau spécifique."""
        disponibilite, created = Disponibilite.objects.get_or_create(
            enseignant=self.enseignant,
            jour=jour,
            creneau=creneau,
            defaults={'est_disponible': est_disponible}
        )
        if not created:
            disponibilite.est_disponible = est_disponible
            disponibilite.save()

    def supprimer_disponibilite(self, jour, creneau):
        """Supprime la disponibilité de l'enseignant pour un créneau spécifique."""
        disponibilite = Disponibilite.objects.filter(
            enseignant=self.enseignant,
            jour=jour,
            creneau=creneau
        )
        disponibilite.delete()

    def get_disponibilites(self):
        """Retourne les disponibilités de l'enseignant."""
        return Disponibilite.objects.filter(enseignant=self.enseignant)


class GestionAffectation:
    def __init__(self, matiere, groupe, enseignant, type_seance):
        self.matiere = matiere
        self.groupe = groupe
        self.enseignant = enseignant
        self.type_seance = type_seance

    def affecter(self):
        """Affecte un enseignant à une matière, un groupe et un type de séance."""
        affectation, created = Affectation.objects.get_or_create(
            matiere=self.matiere,
            groupe=self.groupe,
            enseignant=self.enseignant,
            type=self.type_seance
        )
        return affectation

    def annuler_affectation(self):
        """Annule l'affectation d'un enseignant à une matière et un groupe pour un type de séance."""
        Affectation.objects.filter(
            matiere=self.matiere,
            groupe=self.groupe,
            enseignant=self.enseignant,
            type=self.type_seance
        ).delete()

    def get_affectations(self):
        """Retourne toutes les affectations pour un groupe et une matière."""
        return Affectation.objects.filter(matiere=self.matiere, groupe=self.groupe)


class GestionEmploiDuTemps:
    def __init__(self, groupe, semaine=None):
        self.groupe = groupe
        self.semaine = semaine

    def ajouter_cours(self, matiere, enseignant, jour, creneau, type_seance):
        """Ajoute un cours à l'emploi du temps du groupe."""
        emploi, created = CreneauEmploiDuTemps.objects.get_or_create(
            groupe=self.groupe,
            matiere=matiere,
            enseignant=enseignant,
            jour=jour,
            creneau=creneau,
            type=type_seance
        )
        if not created:
            # Si le créneau existe déjà, on le met à jour.
            emploi.type = type_seance
            emploi.save()
        return emploi

    def supprimer_cours(self, matiere, enseignant, jour, creneau):
        """Supprime un cours de l'emploi du temps."""
        CreneauEmploiDuTemps.objects.filter(
            groupe=self.groupe,
            matiere=matiere,
            enseignant=enseignant,
            jour=jour,
            creneau=creneau
        ).delete()

    def get_emplois(self):
        """Retourne tous les emplois du temps pour le groupe."""
        return CreneauEmploiDuTemps.objects.filter(groupe=self.groupe)

    def verifier_chevauchement(self, matiere, jour, creneau):
        """Vérifie si un créneau chevauche un autre dans l'emploi du temps."""
        emplois = CreneauEmploiDuTemps.objects.filter(
            groupe=self.groupe,
            jour=jour,
            creneau=creneau
        )
        for emploi in emplois:
            if emploi.matiere != matiere:
                return True  # Un chevauchement existe
        return False


class GestionCharge:
    def __init__(self, matiere, groupe):
        self.matiere = matiere
        self.groupe = groupe

    def definir_charge(self, cm=0, tp=0, td=0):
        """Définit ou met à jour la charge de travail pour un groupe et une matière."""
        charge, created = Charge.objects.get_or_create(
            matiere=self.matiere,
            groupe=self.groupe,
            defaults={'cm': cm, 'tp': tp, 'td': td}
        )
        if not created:
            charge.cm = cm
            charge.tp = tp
            charge.td = td
            charge.save()
        return charge

    def obtenir_charge(self):
        """Retourne la charge actuelle pour une matière et un groupe."""
        return Charge.objects.get(matiere=self.matiere, groupe=self.groupe)


class GestionChevauchement:
    def __init__(self, groupe1, groupe2):
        self.groupe1 = groupe1
        self.groupe2 = groupe2

    def definir_chevauchement(self, autorise):
        """Définit si deux groupes peuvent avoir des cours en chevauchement.""" 
        chevauchement, created = Chevauchement.objects.get_or_create(
            groupe1=self.groupe1,
            groupe2=self.groupe2,
            defaults={'chevauchement': autorise}
        )
        if not created:
            chevauchement.chevauchement = autorise
            chevauchement.save()
        return chevauchement

    def obtenir_chevauchement(self):
        """Retourne le statut de chevauchement entre deux groupes."""
        return Chevauchement.objects.get(groupe1=self.groupe1, groupe2=self.groupe2)