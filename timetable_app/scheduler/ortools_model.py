import pandas as pd
from ortools.linear_solver import pywraplp
import openpyxl

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
        self.Dik = []
        self.Groupes = ['G1', 'G2', 'TP1', 'TP2', 'TP3', 'TP4', 'CNM', 'RSS', 'DSI_CM', 'DIS_TP1', 'DSI_TP2']
        self.G = len(self.Groupes)
        self.S = 4  # Nombre de salles
        self.K = 25  # Nombre de créneaux
        self.STP = 2  # Nombre de salles de TP
        self.ind = self.generate_indices()

    def generate_indices(self):
        col = ['B', 'C', 'D', 'E', 'F']
        lin = ['4', '5', '6', '8', '9']
        return [i + j for i in col for j in lin]

    def load_data(self):
        # Load Matières
        M = pd.read_excel(self.data_file, sheet_name=3)
        self.Matieres = [M['Unnamed: 0'][i] for i in range(3, 12)]

        # Load Charges (Pcm, Ptp, Ptd)
        M1 = pd.read_excel(self.data_file, sheet_name=3)
        c = [f'Unnamed: {i}' for i in range(1, 34)]
        for j in range(3, 12):
            self.Pcm.append([M1[c[i]][j] for i in range(0, len(c), 3)])
            self.Ptp.append([M1[c[i + 1]][j] for i in range(0, len(c), 3)])
            self.Ptd.append([M1[c[i + 2]][j] for i in range(0, len(c), 3)])

        # Load Profs
        B = pd.read_excel(self.data_file, sheet_name=1)
        self.profs = [B['Unnamed: 0'][i] for i in range(1, 18)]
        self.I = len(self.profs)

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

        # Load Disponibilité (Dik)
        Di = pd.read_excel(self.data_file, sheet_name=1)
        a = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
        for i in a:
            for j in range(1, 18):
                self.Dik.append(Di[i][j])

    def solve(self):
        solver = pywraplp.Solver.CreateSolver('CBC')
        X = [[[solver.IntVar(0, 1, f'X_{g}_{j}_{k}') for k in range(self.K)] for j in range(len(self.Matieres))] for g in range(self.G)]
        Y = [[[solver.IntVar(0, 1, f'Y_{g}_{j}_{k}') for k in range(self.K)] for j in range(len(self.Matieres))] for g in range(self.G)]
        Z = [[[solver.IntVar(0, 1, f'Z_{g}_{j}_{k}') for k in range(self.K)] for j in range(len(self.Matieres))] for g in range(self.G)]

        # Add constraints
        for g in range(self.G):
            for j in range(len(self.Matieres)):
                solver.Add(sum(X[g][j][k] for k in range(self.K)) == self.Pcm[j][g])
                solver.Add(sum(Y[g][j][k] for k in range(self.K)) == self.Ptp[j][g])
                solver.Add(sum(Z[g][j][k] for k in range(self.K)) == self.Ptd[j][g])

        for g in range(self.G):
            for k in range(self.K):
                solver.Add(sum(X[g][j][k] + Y[g][j][k] + Z[g][j][k] for j in range(len(self.Matieres))) <= 1)

        for k in range(self.K):
            solver.Add(sum(X[g][j][k] + Y[g][j][k] + Z[g][j][k] for j in range(len(self.Matieres)) for g in range(self.G)) <= self.S)
            solver.Add(sum(Y[g][j][k] for j in range(len(self.Matieres)) for g in range(self.G)) <= self.STP)

        for i in range(self.I):
            for k in range(self.K):
                solver.Add(sum(X[h[0]][h[1]][k] for h in self.Ccm[i]) + sum(Y[h[0]][h[1]][k] for h in self.Ctp[i]) + sum(Z[h[0]][h[1]][k] for h in self.Ctd[i]) <= self.Dik[i][k])

        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            self.export_results(X, Y, Z)
            return True
        return False

    def export_results(self, X, Y, Z):
        for j in range(len(self.Matieres)):
            for k in range(self.K):
                for g in range(self.G):
                    if X[g][j][k].solution_value() != 0:
                        self.write_to_excel('1emploi.xlsx', self.ind[k], f'{self.Groupes[g]}/CM: {self.Matieres[j]}')
                    if Y[g][j][k].solution_value() != 0:
                        self.write_to_excel('1emploi.xlsx', self.ind[k], f'{self.Groupes[g]}/TP: {self.Matieres[j]}')
                    if Z[g][j][k].solution_value() != 0:
                        self.write_to_excel('1emploi.xlsx', self.ind[k], f'{self.Groupes[g]}/TD: {self.Matieres[j]}')

    def write_to_excel(self, file_name, cell, value):
        wb = openpyxl.load_workbook(file_name)
        ws = wb.active
        ws[cell].value = value
        wb.save(file_name)