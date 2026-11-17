import math
import random

INF = float("inf")   # "-" dans l'énoncé : pas de route entre les deux villes

# Distances entre les 8 villes (matrice symétrique, la ville 1 est à l'indice 0)
#                  1    2    3    4    5    6    7    8
matrice_distances = [
                 [  0,  14,  15, INF, INF, INF, INF,  17],   # 1
                 [ 14,   0,  13,  14,  20, INF, INF,  21],   # 2
                 [ 15,  13,   0,  11,  21,  17,   9,   9],   # 3
                 [INF,  14,  11,   0,  11,  10,   8,  20],   # 4
                 [INF,  20,  21,  11,   0,  15,  18, INF],   # 5
                 [INF, INF,  17,  10,  15,   0,   9, INF],   # 6
                 [INF, INF,   9,   8,  18,   9,   0,  13],   # 7
                 [ 17,  21,   9,  20, INF, INF,  13,   0]]   # 8


def distance(a, b):
    # Distance entre la ville a et la ville b (villes numérotées de 1 à 8)
    return matrice_distances[a - 1][b - 1]


def calculer_distance_totale(solution):
    # Somme des distances du tour, y compris le retour à la ville de départ
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += distance(solution[i], solution[i + 1])
    distance_totale += distance(solution[-1], solution[0])
    return distance_totale


def afficher_tour(solution):
    # [1, 2, 3] -> "1-2-3-1"
    return "-".join(str(v) for v in solution + [solution[0]])


def generer_voisin_aleatoire(solution):
    # Échanger 2 villes choisies au hasard (la ville 1 reste au départ).
    # On recommence tant que le tour utilise une route qui n'existe pas.
    while True:
        voisin = solution[:]
        i, j = random.sample(range(1, len(solution)), 2)
        voisin[i], voisin[j] = voisin[j], voisin[i]
        if calculer_distance_totale(voisin) != INF:
            return voisin, voisin[i], voisin[j]


def recuit_simule(solution_initiale, nombre_iterations, temperature, alpha):
    solution_actuelle = solution_initiale[:]
    distance_actuelle = calculer_distance_totale(solution_actuelle)
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = distance_actuelle
    print(f"Solution initiale : {afficher_tour(solution_actuelle)}  distance = {distance_actuelle}")

    for iteration in range(1, nombre_iterations + 1):
        voisin, a, b = generer_voisin_aleatoire(solution_actuelle)
        distance_voisin = calculer_distance_totale(voisin)
        delta = distance_voisin - distance_actuelle

        print(f"\nItération {iteration}  (T = {temperature:.1f})")
        print(f"  Échange {a} et {b} : {afficher_tour(voisin)}  distance = {distance_voisin}  delta = {delta}")

        if delta <= 0:
            accepte = True
            print("  Meilleur (ou égal) -> accepté")
        else:
            # Moins bon : accepté avec la probabilité exp(-delta / T)
            probabilite = math.exp(-delta / temperature)
            r = random.random()
            accepte = r < probabilite
            print(f"  Moins bon : P = exp(-{delta}/{temperature:.1f}) = {probabilite:.3f}, "
                  f"r = {r:.3f} -> {'accepté' if accepte else 'refusé'}")

        if accepte:
            solution_actuelle = voisin
            distance_actuelle = distance_voisin
            if distance_actuelle < meilleure_distance:
                meilleure_solution = solution_actuelle[:]
                meilleure_distance = distance_actuelle

        print(f"  Solution actuelle : {afficher_tour(solution_actuelle)}  "
              f"distance = {distance_actuelle}  | meilleure = {meilleure_distance}")

        # Variation empirique de la température : T diminue à chaque itération
        temperature = alpha * temperature

    return meilleure_solution, meilleure_distance


solution_initiale = [1, 2, 3, 4, 5, 6, 7, 8]
nombre_iterations = 5
temperature_initiale = 20
alpha = 0.8

meilleure_solution, meilleure_distance = recuit_simule(solution_initiale, nombre_iterations,
                                                       temperature_initiale, alpha)

print("\nMeilleure solution trouvée (Recuit simulé) :", afficher_tour(meilleure_solution))
print("Distance minimale :", meilleure_distance)
