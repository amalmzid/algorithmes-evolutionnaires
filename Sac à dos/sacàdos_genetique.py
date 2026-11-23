import random

#valeurs[i] et poids[i] : valeur et poids de l'objet i
valeurs = [10, 5, 15, 7, 6, 18, 3, 12, 9, 8]
poids = [2, 3, 5, 7, 1, 4, 1, 6, 3, 2]
#poids maximal que le sac peut contenir
capacite = 15
#nombre d'objets dans un chromosome (un individu = une liste de 0 et de 1 : 1 = objet pris, 0 = objet non pris)
nombre_objets = 10
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

#pour calculer le poids total d'un individu
def poids_total(individu):
    pt = 0
    for i in range(nombre_objets):
        if(individu[i] == 1):
            pt += poids[i]
    return pt

#pour calculer la valeur totale d'un individu : c'est le score, on cherche le MAXIMUM
def valeur_totale(individu):
    vt = 0
    for i in range(nombre_objets):
        if(individu[i] == 1):
            vt += valeurs[i]
    return vt


#pour reparer un individu qui depasse la capacite : on retire des objets au hasard jusqu'a respecter le poids
#(apres reparation, tous les individus sont valides)
def reparer(individu):
    pris = [i for i in range(nombre_objets) if individu[i] == 1]
    while(poids_total(individu) > capacite):
        i = random.choice(pris)
        pris.remove(i)
        individu[i] = 0
    return individu


#pour creer un individu (valide)
def creation_individu():
    Indi = [random.randint(0, 1) for i in range(nombre_objets)]
    return reparer(Indi)


#pour creer une generation
def createGeneration():
    generation = []
    for i in range(0, nombre_individu, 1):
        individu = creation_individu()
        while(individu in generation):
            individu = creation_individu()
        generation.append(individu)
    return generation


#pour evaluer une generation : retourne [meilleur score, position du meilleur individu]
#le score est la valeur totale : on cherche le MAXIMUM
def evaluation(generation):
    x = 0
    maxi = valeur_totale(generation[0])
    for i in range(0, len(generation), 1):
        res = valeur_totale(generation[i])
        if(maxi < res):
            maxi = res
            x = i
    son = []
    son.append(maxi)
    son.append(x)
    return son


def afficheGeneration(generation, nombreGeneration):
    res = evaluation(generation)
    print("Generation", nombreGeneration, ": meilleur individu", generation[res[1]], "valeur:", res[0])


#pour faire croisement : ajoute 2 enfants dans init (les enfants sont repares s'ils depassent la capacite)
def croisement(init, individu1, individu2):
    parent1 = individu1
    parent2 = individu2
    gen1 = []
    gen2 = []

    # ---- CROISEMENT A 1 POINT : debut du parent1 + fin du parent2 (et inversement) (METHODE UTILISEE) ----
    position = random.randint(1, nombre_objets - 1)
    gen1 = parent1[:position] + parent2[position:]
    gen2 = parent2[:position] + parent1[position:]

    # ---- CROISEMENT A 2 POINTS : le morceau entre 2 points est echange entre les parents ----
    #point1, point2 = sorted(random.sample(range(nombre_objets), 2))
    #gen1 = parent1[:point1] + parent2[point1:point2 + 1] + parent1[point2 + 1:]
    #gen2 = parent2[:point1] + parent1[point1:point2 + 1] + parent2[point2 + 1:]

    # ---- CROISEMENT UNIFORME : un masque 0/1 choisit, position par position, le parent qui donne l'objet ----
    #masque = [random.randint(0, 1) for i in range(nombre_objets)]
    #gen1 = [parent1[i] if masque[i] == 1 else parent2[i] for i in range(nombre_objets)]
    #gen2 = [parent2[i] if masque[i] == 1 else parent1[i] for i in range(nombre_objets)]

    init.append(reparer(gen1))
    init.append(reparer(gen2))


#pour faire mutation (inverser un objet : pris <-> non pris), puis reparer si le sac est trop lourd
def mutation(individu):
    i = random.randint(0, nombre_objets - 1)
    individu[i] = 1 - individu[i]
    return reparer(individu)


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
#score = valeur totale : plus grande = meilleure
def selection(generation):
    scores = [valeur_totale(x) for x in generation]
    parents = []

    # ---- TOURNOI : on tire 3 individus au hasard, on garde celui qui a la plus grande valeur (METHODE UTILISEE) ----
    while(len(parents) < nombre_individu):
        candidats = random.sample(range(len(generation)), 3)
        meilleur = max(candidats, key=lambda i: scores[i])
        parents.append(generation[meilleur][:])

    # ---- ROULETTE : proba proportionnelle a la valeur (plus grande valeur = plus de chance) ----
    #poids_roulette = [s + 1 for s in scores]
    #while(len(parents) < nombre_individu):
    #    i = random.choices(range(len(generation)), weights=poids_roulette)[0]
    #    parents.append(generation[i][:])

    # ---- RANG : on classe du pire (rang 1) au meilleur (rang N), proba proportionnelle au rang ----
    #indices = sorted(range(len(generation)), key=lambda i: scores[i])
    #rangs = list(range(1, len(generation) + 1))
    #while(len(parents) < nombre_individu):
    #    i = random.choices(indices, weights=rangs)[0]
    #    parents.append(generation[i][:])

    # ---- ELITISTE : seuls les meilleurs (la moitie) peuvent devenir parents ----
    #indices = sorted(range(len(generation)), key=lambda i: scores[i], reverse=True)
    #meilleurs = indices[:nombre_individu // 2]
    #while(len(parents) < nombre_individu):
    #    i = random.choice(meilleurs)
    #    parents.append(generation[i][:])

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
    if(resultat[0] > meilleur_score):
        meilleur_score = resultat[0]
        meilleur_individu = generation[resultat[1]][:]
    #elitisme : le meilleur individu trouve est remis dans la generation
    generation[0] = meilleur_individu[:]
    nombre_generation += 1
    if(nombre_generation % 20 == 0):
        afficheGeneration(generation, nombre_generation)

print('le meilleur individu est : ', meilleur_individu)
print('la valeur maximale est :', meilleur_score)
print('le poids total est :', poids_total(meilleur_individu))
