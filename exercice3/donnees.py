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
