from collections import deque
from donnees import calculer_distance_totale, afficher_tour


def generer_voisins(solution):
    # Un voisin = on échange 2 villes. La ville 1 (position 0) reste au départ.
    voisins = []
    for i in range(1, len(solution)):
        for j in range(i + 1, len(solution)):
            voisin = solution[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins


def tabu_search(solution_initiale, nombre_iterations, taille_tabu):
    solution_actuelle = solution_initiale[:]
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle)
    print(f"Solution initiale : {afficher_tour(solution_actuelle)}  distance = {meilleure_distance}\n")

    tabu_list = deque(maxlen=taille_tabu)
    tabu_list.append(solution_actuelle)

    for iteration in range(1, nombre_iterations + 1):
        voisins = generer_voisins(solution_actuelle)
        voisins = [voisin for voisin in voisins if voisin not in tabu_list]

        if not voisins:
            print("Plus de voisin autorisé -> arrêt")
            break

        # Meilleur voisin non tabou (même s'il est moins bon que la solution actuelle)
        solution_actuelle = min(voisins, key=calculer_distance_totale)
        distance_actuelle = calculer_distance_totale(solution_actuelle)

        tabu_list.append(solution_actuelle)

        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle

        print(f"Itération {iteration:2d} : {afficher_tour(solution_actuelle)}  "
              f"distance = {distance_actuelle}  | meilleure = {meilleure_distance}")

    return meilleure_solution, meilleure_distance


solution_initiale = [1, 2, 3, 4, 5, 6, 7, 8]
nombre_iterations = 10
taille_tabu = 10

meilleure_solution, meilleure_distance = tabu_search(solution_initiale, nombre_iterations, taille_tabu)

print("\nMeilleure solution trouvée (Tabu Search) :", afficher_tour(meilleure_solution))
print("Distance minimale :", meilleure_distance)
