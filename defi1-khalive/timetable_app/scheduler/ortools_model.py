import traceback
import pandas as pd
from ortools.linear_solver import pywraplp
import openpyxl
import numpy as np
import logging
import sys
import os

# Définir le niveau de journalisation sur ERROR pour ne montrer que les erreurs critiques
logging.getLogger('ortools').setLevel(logging.ERROR)

# Optionnel : Rediriger stderr vers null pour supprimer les messages de journalisation (facultatif)
# sys.stderr = open(os.devnull, 'w')

class ScheduleSolver:
    def __init__(self, data_file):
        self.data_file = data_file
        self.Matieres = []
        self.profs = []
        self.Pcm = []
        self.Ptp = []
        self.Ptd = []
        self.Ccm = []
        self.Ctp = []
        self.Ctd = []
        self.Dik = []  # Disponibilité des profs pour chaque créneau horaire
        self.Groupes = ['G1', 'G2', 'TP1', 'TP2', 'TP3', 'TP4', 'CNM', 'RSS', 'DSI_CM', 'DIS_TP1', 'DSI_TP2']
        self.G = len(self.Groupes)
        self.S = 4  # Nombre de salles
        self.K = 25  # Nombre de créneaux horaires
        self.STP = 2  # Nombre de salles de TP
        self.ind = self.generate_indices()

    def generate_indices(self):
        col = ['B', 'C', 'D', 'E', 'F']
        lin = ['4', '5', '6', '8', '9']
        indices = [i + j for i in col for j in lin]
        print("Generated Indices: ", indices)  # Afficher les indices générés
        return indices

    def load_data(self):
        try:
            # Load Matières
            M = pd.read_excel(self.data_file, sheet_name=3)
            self.Matieres = [M['Unnamed: 0'][i] for i in range(3, 12)]
            print("Matieres Loaded: ", self.Matieres)  # Afficher les matières chargées

            # Load Charges (Pcm, Ptp, Ptd)
            M1 = pd.read_excel(self.data_file, sheet_name=3)
            c = [f'Unnamed: {i}' for i in range(1, 34)]
            for j in range(3, 12):
                self.Pcm.append([M1[c[i]][j] for i in range(0, len(c), 3)])
                self.Ptp.append([M1[c[i + 1]][j] for i in range(0, len(c), 3)])
                self.Ptd.append([M1[c[i + 2]][j] for i in range(0, len(c), 3)])
            print("Pcm, Ptp, Ptd Loaded: ", self.Pcm, self.Ptp, self.Ptd)  # Afficher les charges

            # Load Profs
            B = pd.read_excel(self.data_file, sheet_name=1)
            self.profs = [B['Unnamed: 0'][i] for i in range(1, 18)]
            self.I = len(self.profs)
            print("Professors Loaded: ", self.profs)  # Afficher les professeurs

            # Load Affectation (Ccm, Ctp, Ctd)
            D = pd.read_excel(self.data_file, sheet_name=4)
            for i in range(self.I):
                self.Ccm.append([])
                self.Ctp.append([])
                self.Ctd.append([])

            for j in range(3, 12):
                for k in range(0, len(c), 3):
                    for i in range(self.I):
                        if D[c[k]][j] == self.profs[i]:
                            self.Ccm[i].append([k // 3, j - 3])
                        if D[c[k + 1]][j] == self.profs[i]:
                            self.Ctp[i].append([k // 3, j - 3])
                        if D[c[k + 2]][j] == self.profs[i]:
                            self.Ctd[i].append([k // 3, j - 3])
            print("Ccm, Ctp, Ctd Loaded: ", self.Ccm, self.Ctp, self.Ctd)  # Afficher l'affectation des profs

            # Load Disponibilité (Dik)
            Di = pd.read_excel(self.data_file, sheet_name=1)
            jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']

            # Initialiser self.Dik comme un tableau 2D
            self.Dik = np.zeros((self.I, self.K), dtype=np.int64)

            for i in range(self.I):
                for j, jour in enumerate(jours):
                    if jour in Di.columns:
                        for k in range(self.K):
                            if Di[jour][i] == 1:  # Si le professeur i est disponible pour le créneau k
                                self.Dik[i][k] = 1  # Marquer la disponibilité
            print("Dik (Disponibilité Professeurs): \n", self.Dik)  # Afficher la disponibilité des profs
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
            print("Traceback: ")
            print(traceback.format_exc())  # Affiche la trace complète de l'erreur pour plus de détails

    def reset_model(self, solver):
        """Réinitialise les variables de décision avant chaque nouvelle résolution."""
        try:
            self.X = [[[solver.IntVar(0, 1, f'X_{g}_{j}_{k}') for k in range(self.K)] for j in range(len(self.Matieres))] for g in range(self.G)]
            self.Y = [[[solver.IntVar(0, 1, f'Y_{g}_{j}_{k}') for k in range(self.K)] for j in range(len(self.Matieres))] for g in range(self.G)]
            self.Z = [[[solver.IntVar(0, 1, f'Z_{g}_{j}_{k}') for k in range(self.K)] for j in range(len(self.Matieres))] for g in range(self.G)]
            
            print("Variables re-initialisées.")
        except Exception as e:
            print(f"Erreur lors de la réinitialisation du modèle : {e}")
            print("Traceback: ")
            print(traceback.format_exc())  # Affiche la trace complète de l'erreur

    def solve(self):
        try:
            # Créer un nouveau solveur à chaque résolution pour éviter les conflits
            solver = pywraplp.Solver.CreateSolver('GLOP')  # Créer le solveur (GLOP ou autre)

            if not solver:
                raise Exception("Le solveur n'a pas pu être créé.")

            # Réinitialiser les variables de décision avant chaque solution
            self.reset_model(solver)

            # Ajouter les contraintes au solveur
            for g in range(self.G):
                for j in range(len(self.Matieres)):
                    solver.Add(sum(self.X[g][j][k] for k in range(self.K)) == self.Pcm[j][g])
                    solver.Add(sum(self.Y[g][j][k] for k in range(self.K)) == self.Ptp[j][g])
                    solver.Add(sum(self.Z[g][j][k] for k in range(self.K)) == self.Ptd[j][g])

            # Relaxation: Permettre plus de flexibilité dans les créneaux horaires
            for g in range(self.G):
                for k in range(self.K):
                    solver.Add(sum(self.X[g][j][k] + self.Y[g][j][k] + self.Z[g][j][k] for j in range(len(self.Matieres))) <= 2)

            # Résoudre le modèle
            status = solver.Solve()

            if status == pywraplp.Solver.OPTIMAL:
                print("Le modèle a été résolu avec succès !")
                self.export_results()
                return True
            else:
                print(f"Erreur : Le modèle n'a pas trouvé une solution optimale. Code d'état: {status}")
                raise Exception(f"Erreur dans la résolution: Code d'état: {status}")

        except Exception as e:
            print(f"Erreur lors de la résolution du modèle : {e}")
            print("Traceback: ")
            print(traceback.format_exc())  # Affiche la trace complète de l'erreur

    # Fonction pour afficher et exporter les résultats
    def export_results(self):
        try:
            for j in range(len(self.Matieres)):
                for k in range(self.K):
                    for g in range(self.G):
                        if self.X[g][j][k].solution_value() != 0:
                            self.write_to_excel('1emploi.xlsx', self.ind[k], f'{self.Groupes[g]}/CM: {self.Matieres[j]}')
                        if self.Y[g][j][k].solution_value() != 0:
                            self.write_to_excel('1emploi.xlsx', self.ind[k], f'{self.Groupes[g]}/TP: {self.Matieres[j]}')
                        if self.Z[g][j][k].solution_value() != 0:
                            self.write_to_excel('1emploi.xlsx', self.ind[k], f'{self.Groupes[g]}/TD: {self.Matieres[j]}')
            print("Results Exported to Excel.")  # Afficher un message une fois que les résultats sont exportés
        except Exception as e:
            print(f"Erreur lors de l'exportation des résultats : {e}")
            print("Traceback: ")
            print(traceback.format_exc())  # Affiche la trace complète de l'erreur

    def write_to_excel(self, file_name, cell, value):
        try:
            wb = openpyxl.load_workbook(file_name)
            ws = wb.active
            ws[cell].value = value
            wb.save(file_name)
            print(f"Written to Excel at {cell}: {value}")  # Afficher un message à chaque écriture dans Excel
        except Exception as e:
            print(f"Error writing to Excel: {e}")
            print("Traceback: ")
            print(traceback.format_exc())  # Affiche la trace complète de l'erreur

    def get_schedule(self):
        try:
            schedule = {}

            for j in range(len(self.Matieres)):
                for k in range(self.K):
                    for g in range(self.G):
                        if self.X[g][j][k].solution_value() != 0:
                            group = self.Groupes[g]
                            subject = f'{self.Matieres[j]} (CM)'
                            if group not in schedule:
                                schedule[group] = {}
                            if k not in schedule[group]:
                                schedule[group][k] = []
                            schedule[group][k].append(subject)

                        if self.Y[g][j][k].solution_value() != 0:
                            group = self.Groupes[g]
                            subject = f'{self.Matieres[j]} (TP)'
                            if group not in schedule:
                                schedule[group] = {}
                            if k not in schedule[group]:
                                schedule[group][k] = []
                            schedule[group][k].append(subject)

                        if self.Z[g][j][k].solution_value() != 0:
                            group = self.Groupes[g]
                            subject = f'{self.Matieres[j]} (TD)'
                            if group not in schedule:
                                schedule[group] = {}
                            if k not in schedule[group]:
                                schedule[group][k] = []
                            schedule[group][k].append(subject)

            print("Schedule Generated: ", schedule)
            return schedule  # Retourne l'emploi du temps généré
        except Exception as e:
            print(f"Erreur lors de la génération de l'emploi du temps : {e}")
            print("Traceback: ")
            print(traceback.format_exc())  # Affiche la trace complète de l'erreur

if __name__ == "__main__":
    solver = ScheduleSolver('Données.xlsx')
    solver.load_data()
    if solver.solve():
        schedule = solver.get_schedule()
        print(schedule)  # Affiche l'emploi du temps complet