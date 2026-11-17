import random
from collections import deque

INF = float("inf")   # "-" dans l'énoncé : pas de route entre les deux villes


def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale


def generer_voisins(solution):
    voisins = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            voisin = solution[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins


def tabu_search(matrice_distances, nombre_iterations, taille_tabu):
    nombre_villes = len(matrice_distances)
    solution_actuelle = list(range(nombre_villes))

    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)

    tabu_list = deque(maxlen=taille_tabu)

    for _ in range(nombre_iterations):
        voisins = generer_voisins(solution_actuelle)
        voisins = [voisin for voisin in voisins if voisin not in tabu_list]

        if not voisins:
            break

        solution_actuelle = min(voisins, key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)

        tabu_list.append(solution_actuelle)

        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle

    return meilleure_solution, meilleure_distance


# Distances entre les 8 villes (matrice symétrique, la ville 1 est à l'indice 0)
matrice_distances = [
    [  0,  14,  15, INF, INF, INF, INF,  17],
    [ 14,   0,  13,  14,  20, INF, INF,  21],
    [ 15,  13,   0,  11,  21,  17,   9,   9],
    [INF,  14,  11,   0,  11,  10,   8,  20],
    [INF,  20,  21,  11,   0,  15,  18, INF],
    [INF, INF,  17,  10,  15,   0,   9, INF],
    [INF, INF,   9,   8,  18,   9,   0,  13],
    [ 17,  21,   9,  20, INF, INF,  13,   0]
]

nombre_iterations = 10
taille_tabu = 10

meilleure_solution, meilleure_distance = tabu_search(matrice_distances, nombre_iterations, taille_tabu)

print("Meilleure solution trouvée (Tabu Search):", meilleure_solution)
print("Distance minimale:", meilleure_distance)
