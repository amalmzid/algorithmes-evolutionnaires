import random


CAPACITES = [20, 15, 35, 40, 15, 15, 10]   # unités 1 à 7
DEMANDES = [80, 90, 65, 70]                # intervalles 1 à 4
CAPACITE_TOTALE = sum(CAPACITES)           # 150 MW

GENES_POSSIBLES = [
    ["1100", "0110", "0011"],              # unité 1
    ["1100", "0110", "0011"],              # unité 2
    ["1000", "0100", "0010", "0001"],      # unité 3
    ["1000", "0100", "0010", "0001"],      # unité 4
    ["1000", "0100", "0010", "0001"],      # unité 5
    ["1000", "0100", "0010", "0001"],      # unité 6
    ["1000", "0100", "0010", "0001"],      # unité 7
]



TAILLE_POPULATION = 42   # règle : 6 à 7 fois le nb de variables (7 unités)
NB_GENERATIONS = 20
PROBA_CROISEMENT = 0.8   # pc
PROBA_MUTATION = 0.2     # pm 


def reserves(chromosome):
    # Réserve de chaque intervalle = capacité totale - puissance en maintenance - demande
    resultat = []
    for t in range(4):
        perdue = sum(CAPACITES[i] for i, gene in enumerate(chromosome) if gene[t] == "1")
        resultat.append(CAPACITE_TOTALE - perdue - DEMANDES[t])
    return resultat


def fitness(chromosome):
    # La performance = la plus petite réserve (0 si elle est négative)
    return max(0, min(reserves(chromosome)))


def afficher(chromosome):
    return " ".join(chromosome)


def population_initiale(taille):
    # Pour chaque unité, on tire au hasard une maintenance possible
    return [[random.choice(options) for options in GENES_POSSIBLES] for _ in range(taille)]


# Sélection par loterie 

def selection_loterie(population):
   
    poids = [fitness(c) for c in population]
    if sum(poids) == 0:   
        return random.choice(population)
    return random.choices(population, weights=poids)[0]


# Croisement (sur des blocs de 4 bits)

def croisement(parent1, parent2):
    # Croisement 1 point entre deux gènes : on échange les fins des parents
    c = random.randint(1, len(parent1) - 1)
    return parent1[:c] + parent2[c:], parent2[:c] + parent1[c:]


# Mutations (sur des blocs de 4 bits)

def mutation_inversion(chromosome):
    # Pour chaque gène, avec la probabilité pm : on inverse l'ordre d'un morceau du gène
    chromosome = chromosome[:]
    for i, gene in enumerate(chromosome):
        if random.random() < PROBA_MUTATION:
            a, b = sorted(random.sample(range(5), 2))
            nouveau = gene[:a] + gene[a:b][::-1] + gene[b:]
            if nouveau in GENES_POSSIBLES[i]:   
                chromosome[i] = nouveau
    return chromosome


def mutation_remplacement(chromosome):
    # Autre mutation : on remplace le gène par une autre maintenance possible
    chromosome = chromosome[:]
    for i in range(len(chromosome)):
        if random.random() < PROBA_MUTATION:
            chromosome[i] = random.choice(GENES_POSSIBLES[i])
    return chromosome


# Algorithme génétique

def algorithme_genetique(population, mutation):
    for generation in range(1, NB_GENERATIONS + 1):
        meilleur = max(population, key=fitness)
        nouvelle = [meilleur[:]]   # élitisme : le meilleur passe directement
        while len(nouvelle) < len(population):
            parent1, parent2 = selection_loterie(population), selection_loterie(population)
            if random.random() < PROBA_CROISEMENT:
                enfant1, enfant2 = croisement(parent1, parent2)
            else:
                enfant1, enfant2 = parent1[:], parent2[:]
            nouvelle += [mutation(enfant1), mutation(enfant2)]
        population = nouvelle[:len(population)]

        meilleur = max(population, key=fitness)
        moyenne = sum(fitness(c) for c in population) / len(population)
        print(f"Génération {generation:2d} : {afficher(meilleur)}  fitness = {fitness(meilleur)}  moyenne = {moyenne:.1f}")
    return meilleur


population = population_initiale(TAILLE_POPULATION)

resultats = {}
for nom, mutation in (("inversion", mutation_inversion), ("remplacement", mutation_remplacement)):
    print(f"\nMutation par {nom}")
    resultats[nom] = algorithme_genetique(population, mutation)

print("\nRésultats")
for nom, meilleur in resultats.items():
    print(f"{nom:12}  {afficher(meilleur)}  réserves = {reserves(meilleur)}  fitness = {fitness(meilleur)}")
