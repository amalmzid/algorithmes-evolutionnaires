import random

# Données du problème
#                    M1  M2  M3
matrice_couts = [[5,  3,  4],    # D1
                 [6,  7,  2]]    # D2
offres = [8, 9]          # containers disponibles dans D1, D2
demandes = [4, 5, 8]     # containers commandes par M1, M2, M3

# un gène = une case (depot, magasin)
cases = [(i, j) for i in range(len(offres)) for j in range(len(demandes))]
# nombre de gènes dans un chromosome
nombre_gene = len(cases)
# nombre d'individus dans une génération
nombre_individu = 5
# nombre de générations
max_generation = 30
# pour génération
generation = []


# un individu = l'ordre dans lequel on remplit les cases
# chaque case reçoit le maximum possible, donc la solution respecte toujours offres et demandes
def creation_individu():
    individu = cases[:]
    random.shuffle(individu)
    return individu


# pour créer une génération
def createGeneration():
    generation = []
    for i in range(0, nombre_individu, 1):
        individu = creation_individu()
        while individu in generation:
            individu = creation_individu()
        generation.append(individu)
    return generation


# pour transformer un individu en solution (matrice de containers)
def decoder(individu):
    reste_offre = offres[:]
    reste_demande = demandes[:]
    solution = [[0] * len(demandes) for _ in range(len(offres))]
    for i, j in individu:
        quantite = min(reste_offre[i], reste_demande[j])
        solution[i][j] = quantite
        reste_offre[i] -= quantite
        reste_demande[j] -= quantite
    return solution


# pour calculer le coût total d'un individu
def cout(individu):
    solution = decoder(individu)
    cout_total = 0
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            cout_total += matrice_couts[i][j] * solution[i][j]
    return cout_total


# pour faire croisement
def croisement_point(init, individu1, individu2, position):
    parent1 = individu1
    parent2 = individu2
    gen1 = parent1[:position]
    gen2 = parent2[:position]
    # on complète avec les cases manquantes, dans l'ordre de l'autre parent (sans doublon)
    gen1 += [case for case in parent2 if case not in gen1]
    gen2 += [case for case in parent1 if case not in gen2]
    init.append(gen1)
    init.append(gen2)


# pour faire mutation
def mutation(individu, position):  # position de la mutation
    individu = individu[:]
    autre = random.choice([p for p in range(nombre_gene) if p != position])
    individu[position], individu[autre] = individu[autre], individu[position]
    return individu


# pour développer une génération
def developpement_generation(generation1, position_croisement, position_mutation):
    croisement_point(generation1, generation1[1], generation1[2], position_croisement)
    croisement_point(generation1, generation1[3], generation1[4], position_croisement)
    generation1.append(mutation(generation1[0], position_mutation))


# pour faire sélection
def selection(generation):
    # pour placer les éléments dans l'ordre croissant du coût (le moins cher d'abord)
    generation.sort(key=cout)
    generationfondue = []
    # on garde seulement les meilleurs
    for i in range(nombre_individu):
        generationfondue.append(generation[i])
    return generationfondue


def evaluation(generation):
    x = 0
    min = cout(generation[0])
    son = []
    for i in range(0, len(generation), 1):
        res = cout(generation[i])
        if res < min:
            min = res
            x = i
    son.append(min)
    son.append(x)
    return son


nombre_generation = 1
# génération initiale
generation = createGeneration()

while nombre_generation < max_generation:
    developpement_generation(generation, 3, random.randrange(nombre_gene))
    generation = selection(generation)
    nombre_generation += 1

evaluation_generation = evaluation(generation)
print('Meilleure solution :', decoder(generation[evaluation_generation[1]]))
print('Cout minimal :', evaluation_generation[0])
