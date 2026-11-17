import math
import random

maintenance_centrales_1_2 = ['1100', '0110', '0011']
maintenance_autres_centrales = ['1000', '0100', '0010', '0001']
nombre_centrales = 7
capacite = [20, 15, 35, 40, 15, 15, 10]
capacite_totale = sum(capacite)
demande = [80, 90, 65, 70]


def maintenances_possibles(centrale):
    return maintenance_centrales_1_2 if centrale < 2 else maintenance_autres_centrales


def generer_solution_initiale():
    return [random.choice(maintenances_possibles(i)) for i in range(nombre_centrales)]


def calculer_reserve_minimale(solution):
    reserves = []
    for intervalle in range(4):
        puissance_perdue = sum(int(solution[j][intervalle]) * capacite[j] for j in range(nombre_centrales))
        reserves.append(capacite_totale - puissance_perdue - demande[intervalle])
    return max(0, min(reserves))


def generer_voisin(solution):
    voisin = solution[:]
    i = random.randrange(nombre_centrales)
    voisin[i] = random.choice([m for m in maintenances_possibles(i) if m != solution[i]])
    return voisin


def recuit_simule(temperature_initiale, temperature_finale, alpha, iterations_par_palier):
    solution_actuelle = generer_solution_initiale()
    reserve_actuelle = calculer_reserve_minimale(solution_actuelle)

    meilleure_solution = solution_actuelle[:]
    meilleure_reserve = reserve_actuelle

    temperature = temperature_initiale

    while temperature > temperature_finale:
        for _ in range(iterations_par_palier):
            voisin = generer_voisin(solution_actuelle)
            reserve_voisin = calculer_reserve_minimale(voisin)
            delta = reserve_voisin - reserve_actuelle

            if delta >= 0 or random.random() < math.exp(delta / temperature):
                solution_actuelle = voisin
                reserve_actuelle = reserve_voisin

                if reserve_actuelle > meilleure_reserve:
                    meilleure_solution = solution_actuelle[:]
                    meilleure_reserve = reserve_actuelle

        temperature *= alpha

    return meilleure_solution, meilleure_reserve


temperature_initiale = 50
temperature_finale = 0.1
alpha = 0.9
iterations_par_palier = 10

meilleure_solution, meilleure_reserve = recuit_simule(temperature_initiale, temperature_finale, alpha, iterations_par_palier)

print("Meilleure solution trouvée (Recuit simulé):", meilleure_solution)
print("Réserve minimale:", meilleure_reserve)
