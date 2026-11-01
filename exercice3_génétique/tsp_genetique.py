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

TAILLE_POPULATION = 20
NB_GENERATIONS = 10
PROBA_CROISEMENT = 0.8   # pc
PROBA_MUTATION = 0.2     # pm


def calculer_distance_totale(solution):
    # Somme des distances du tour, y compris le retour à la ville de départ
    distance_totale = 0
    for i in range(len(solution)):
        distance_totale += matrice_distances[solution[i] - 1][solution[(i + 1) % len(solution)] - 1]
    return distance_totale


def afficher_tour(solution):
    # [1, 2, 3] -> "1-2-3-1"
    return "-".join(str(v) for v in solution + [solution[0]])


def fitness(solution):
    # Plus le tour est court, plus la fitness est grande. Route "-" : 1/inf = 0
    return 1 / calculer_distance_totale(solution)


def population_initiale(taille):
    # Tours aléatoires : la ville 1 reste au départ, on évite les routes "-"
    population = []
    while len(population) < taille:
        solution = [1] + random.sample(range(2, 9), 7)
        if calculer_distance_totale(solution) != INF:
            population.append(solution)
    return population


# Sélections

def selection_roulette(population):
    # Probabilité proportionnelle à la fitness
    poids = [fitness(s) for s in population]
    return random.choices(population, weights=poids)[0]


def selection_rang(population):
    # On trie du pire au meilleur : le pire a le rang 1, le meilleur le rang N.
    # Probabilité proportionnelle au rang (et non à la fitness)
    classes = sorted(population, key=calculer_distance_totale, reverse=True)
    return random.choices(classes, weights=range(1, len(classes) + 1))[0]


def selection_tournoi(population, k=3):
    # On tire k individus au hasard, le meilleur (le tour le plus court) gagne
    return min(random.sample(population, k), key=calculer_distance_totale)


# Croisement et mutation

def croisement(parent1, parent2):
    # Croisement 1 point : début du parent 1, puis villes manquantes dans l'ordre du parent 2
    c = random.randint(2, len(parent1) - 1)

    def enfant(p1, p2):
        debut = p1[:c]
        return debut + [v for v in p2 if v not in debut]

    return enfant(parent1, parent2), enfant(parent2, parent1)


def mutation(solution):
    # Avec la probabilité pm, on échange 2 villes (la ville 1 ne bouge pas)
    solution = solution[:]
    if random.random() < PROBA_MUTATION:
        i, j = random.sample(range(1, len(solution)), 2)
        solution[i], solution[j] = solution[j], solution[i]
    return solution


# Algorithme génétique

def algorithme_genetique(population, selection):
    for generation in range(1, NB_GENERATIONS + 1):
        meilleur = min(population, key=calculer_distance_totale)
        nouvelle = [meilleur[:]]   # élitisme : le meilleur passe directement
        while len(nouvelle) < len(population):
            parent1, parent2 = selection(population), selection(population)
            if random.random() < PROBA_CROISEMENT:
                enfant1, enfant2 = croisement(parent1, parent2)
            else:
                enfant1, enfant2 = parent1[:], parent2[:]
            nouvelle += [mutation(enfant1), mutation(enfant2)]
        population = nouvelle[:len(population)]

        meilleur = min(population, key=calculer_distance_totale)
        print(f"Génération {generation:2d} : {afficher_tour(meilleur)}  distance = {calculer_distance_totale(meilleur)}")
    return meilleur, calculer_distance_totale(meilleur)


random.seed(1)
population = population_initiale(TAILLE_POPULATION)
print("Population initiale :")
for solution in population:
    print(f"  {afficher_tour(solution)}  distance = {calculer_distance_totale(solution)}")

resultats = {}
for nom, selection in (("roulette", selection_roulette), ("rang", selection_rang), ("tournoi", selection_tournoi)):
    print(f"\nSélection par {nom}")
    resultats[nom] = algorithme_genetique(population, selection)

print("\n Résultats")
for nom, (meilleur, distance) in resultats.items():
    print(f"{nom:9}  {afficher_tour(meilleur)}  distance = {distance}")
