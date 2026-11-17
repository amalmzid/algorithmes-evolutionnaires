import random
from collections import deque

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


def generer_voisins(solution):
    voisins = []
    for i in range(nombre_centrales):
        for maintenance in maintenances_possibles(i):
            if maintenance != solution[i]:
                voisin = solution[:]
                voisin[i] = maintenance
                voisins.append(voisin)
    return voisins


def tabu_search(nombre_iterations, taille_tabu):
    solution_actuelle = generer_solution_initiale()

    meilleure_solution = solution_actuelle[:]
    meilleure_reserve = calculer_reserve_minimale(solution_actuelle)

    tabu_list = deque(maxlen=taille_tabu)
    tabu_list.append(solution_actuelle)

    for _ in range(nombre_iterations):
        voisins = generer_voisins(solution_actuelle)
        voisins = [voisin for voisin in voisins if voisin not in tabu_list]

        if not voisins:
            break

        solution_actuelle = max(voisins, key=calculer_reserve_minimale)
        reserve_actuelle = calculer_reserve_minimale(solution_actuelle)

        tabu_list.append(solution_actuelle)

        if reserve_actuelle > meilleure_reserve:
            meilleure_solution = solution_actuelle[:]
            meilleure_reserve = reserve_actuelle

    return meilleure_solution, meilleure_reserve


nombre_iterations = 100
taille_tabu = 10

meilleure_solution, meilleure_reserve = tabu_search(nombre_iterations, taille_tabu)

print("Meilleure solution trouvée (Tabu Search):", meilleure_solution)
print("Réserve minimale:", meilleure_reserve)
