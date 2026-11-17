import random

#distance entre les villes
matrice_distances = [
    [0, 2, 2, 7, 15, 2, 5, 7, 6, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [2, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [7, 10, 4, 2, 0, 7, 3, 2, 2, 7],
    [2, 3, 3, 7, 7, 0, 1, 7, 2, 10],
    [5, 7, 3, 7, 3, 1, 0, 2, 1, 3],
    [7, 7, 4, 7, 2, 7, 2, 0, 1, 10],
    [6, 8, 2, 5, 2, 2, 1, 1, 0, 15],
    [5, 2, 3, 4, 7, 10, 3, 10, 15, 0]
]
#nombre de villes dans un chromosome (un individu = un ordre de visite)
nombre_villes = 10
#nombre d'individu dans une generation (regle : 6 ou 7 fois le nombre de variables)
nombre_individu = 70
#nombre de generation
max_generation = 200
#probabilite de croisement
probabilite_croisement = 0.9
#probabilite de mutation
probabilite_mutation = 0.3
#pour generation
generation = []


#pour calculer la distance totale d'un individu (avec le retour a la ville de depart)
def distance_totale(individu):
    distance = 0
    for i in range(nombre_villes - 1):
        distance += matrice_distances[individu[i]][individu[i + 1]]
    distance += matrice_distances[individu[-1]][individu[0]]
    return distance


#pour creer un individu
def creation_individu():
    Indi = list(range(nombre_villes))
    random.shuffle(Indi)
    return Indi


#pour creer une generation
def createGeneration():
    generation = []
    for i in range(0, nombre_individu, 1):
        individu = creation_individu()
        #madem sna3t individue nzid nesna3 we7ed e5er  bech yjiw lkollhem unique
        while(individu in generation):
            individu = creation_individu()
        generation.append(individu)
    return generation


#pour evaluer une generation : retourne [meilleur score, position du meilleur individu]
#le score est la distance totale : on cherche le MINIMUM
def evaluation(generation):
    x = 0
    mini = distance_totale(generation[0])
    for i in range(0, len(generation), 1):
        res = distance_totale(generation[i])
        if(mini > res):
            mini = res
            x = i
    son = []
    son.append(mini)
    son.append(x)
    return son


def afficheGeneration(generation, nombreGeneration):
    res = evaluation(generation)
    print("Generation", nombreGeneration, ": meilleur individu", generation[res[1]], "distance:", res[0])


#pour completer un enfant : les cases vides (None) recoivent les villes manquantes
#dans l'ordre du parent (l'enfant reste une permutation : chaque ville une seule fois)
def completer(enfant, parent):
    restantes = [ville for ville in parent if ville not in enfant]
    k = 0
    for i in range(len(enfant)):
        if(enfant[i] is None):
            enfant[i] = restantes[k]
            k += 1
    return enfant


#pour faire croisement : ajoute 2 enfants dans init
def croisement(init, individu1, individu2):
    parent1 = individu1
    parent2 = individu2
    gen1 = []
    gen2 = []

    # ---- CROISEMENT A 1 POINT : debut du parent1, puis les villes restantes dans l'ordre du parent2 (METHODE UTILISEE) ----
    position = random.randint(1, nombre_villes - 1)
    gen1 = parent1[:position] + [None] * (nombre_villes - position)
    gen2 = parent2[:position] + [None] * (nombre_villes - position)
    completer(gen1, parent2)
    completer(gen2, parent1)

    # ---- CROISEMENT A 2 POINTS : morceau du parent1 entre 2 points, le reste dans l'ordre du parent2 ----
    # point1, point2 = sorted(random.sample(range(nombre_villes), 2))
    # gen1 = [None] * nombre_villes
    # gen2 = [None] * nombre_villes
    # gen1[point1:point2 + 1] = parent1[point1:point2 + 1]
    # gen2[point1:point2 + 1] = parent2[point1:point2 + 1]
    # completer(gen1, parent2)
    # completer(gen2, parent1)

    # ---- CROISEMENT UNIFORME : un masque 0/1 choisit, position par position, le parent qui donne la ville ----
    # masque = [random.randint(0, 1) for i in range(nombre_villes)]
    # gen1 = [parent1[i] if masque[i] == 1 else None for i in range(nombre_villes)]
    # gen2 = [parent2[i] if masque[i] == 1 else None for i in range(nombre_villes)]
    # completer(gen1, parent2)
    # completer(gen2, parent1)

    init.append(gen1)
    init.append(gen2)


#pour faire mutation (echange de 2 villes)
def mutation(individu):
    i, j = random.sample(range(nombre_villes), 2)
    individu[i], individu[j] = individu[j], individu[i]
    return individu


#pour developper une generation : les parents (choisis par la selection) se croisent deux par deux,
#puis les enfants peuvent muter. Les enfants forment la nouvelle generation.
def developpement_generation(parents):
    enfants = []
    for i in range(0, nombre_individu - 1, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        if(random.random() < probabilite_croisement):
            croisement(enfants, parent1, parent2)
        else:
            enfants.append(parent1[:])
            enfants.append(parent2[:])
    for enfant in enfants:
        if(random.random() < probabilite_mutation):
            mutation(enfant)
    return enfants


#pour faire selection : on choisit nombre_individu PARENTS dans la generation
#score = distance totale : plus petite = meilleure
def selection(generation):
    scores = [distance_totale(x) for x in generation]
    parents = []

    # ---- TOURNOI : on tire 3 individus au hasard, on garde celui qui a la plus petite distance (METHODE UTILISEE) ----
    while(len(parents) < nombre_individu):
        candidats = random.sample(range(len(generation)), 3)
        meilleur = min(candidats, key=lambda i: scores[i])
        parents.append(generation[meilleur][:])

    # ---- ROULETTE : proba proportionnelle a 1 / distance (plus petite distance = plus de chance) ----
    # poids = [1 / s for s in scores]
    # while(len(parents) < nombre_individu):
    #     i = random.choices(range(len(generation)), weights=poids)[0]
    #     parents.append(generation[i][:])

    # ---- RANG : on classe du pire (rang 1) au meilleur (rang N), proba proportionnelle au rang ----
    # indices = sorted(range(len(generation)), key=lambda i: scores[i], reverse=True)
    # rangs = list(range(1, len(generation) + 1))
    # while(len(parents) < nombre_individu):
    #     i = random.choices(indices, weights=rangs)[0]
    #     parents.append(generation[i][:])

    # ---- ELITISTE : seuls les meilleurs (la moitie) peuvent devenir parents ----
    # indices = sorted(range(len(generation)), key=lambda i: scores[i])
    # meilleurs = indices[:nombre_individu // 2]
    # while(len(parents) < nombre_individu):
    #     i = random.choice(meilleurs)
    #     parents.append(generation[i][:])

    return parents


nombre_generation = 0
#generation initiale
generation = createGeneration()
resultat = evaluation(generation)
meilleur_score = resultat[0]
meilleur_individu = generation[resultat[1]][:]

while(nombre_generation < max_generation):
    parents = selection(generation)
    generation = developpement_generation(parents)
    #on garde le meilleur individu trouve depuis le debut
    resultat = evaluation(generation)
    if(resultat[0] < meilleur_score):
        meilleur_score = resultat[0]
        meilleur_individu = generation[resultat[1]][:]
    #elitisme : le meilleur individu trouve est remis dans la generation
    generation[0] = meilleur_individu[:]
    nombre_generation += 1
    if(nombre_generation % 20 == 0):
        afficheGeneration(generation, nombre_generation)

print('le meilleur individu est : ', meilleur_individu)
print('le meilleur score est :', meilleur_score)