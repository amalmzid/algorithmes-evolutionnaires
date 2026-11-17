import random

# les cas possibles de maintenance pour 1 & 2
groupe1 = ['1100', '0110', '0011']
# les cas possibles de maintenance pour 3 & 4 & 5 & 6 & 7
groupe2 = ['1000', '0100', '0010', '0001']
# nombre de gènes dans un chromosome
nombre_gene = 7
# nombre d'individus dans une génération
nombre_individu = 5
# nombre de générations
max_generation = 3
capacite_maximum = 150
# capacité de chaque centrale électrique
capacite = [20, 15, 35, 40, 15, 15, 10]
# consommation de l'énergie dans les quatre intervalles de l'année
intervalle = [80, 90, 65, 70]
# pour génération
generation = []
# le maximum globale est 85
max_reserve = []


# pour créer un individu
def creation_individu():
    Indi = []
    for i in range(nombre_gene):
        if i < 2:
            x = random.choice(groupe1)
            Indi.append(x)
        else:
            x = random.choice(groupe2)
            Indi.append(x)
    return Indi


# pour créer une génération
def createGeneration():
    generation = []
    for i in range(0, nombre_individu, 1):
        individu = creation_individu()
        while individu in generation:
            individu = creation_individu()
        generation.append(individu)
    return generation


# pour calculer la puissance de générateur dans les 4 intervalles
def puissance(individu, capacite):
    somme = []
    for i in range(4):
        x = 0
        while True:
            for j in range(7):
                x += int(individu[j][i]) * capacite[j]
            # x == 0 : aucune centrale en maintenance dans cet intervalle, on évite la boucle infinie
            if x > intervalle[i] or x == 0:
                somme.append(x)
                break
    return somme


# reserve_maxi = Capacité_totale - (puissance_perdue_maintenance + demande)
def reser_maxi(intervalle, puiss):
    reserv = []
    j = 0
    for i in range(0, 4, 1):
        reserv.append(puiss[j] - intervalle[j])
        j = j + 1
    return max(reserv)


# pour faire croisement
def croisement_point(init, individu1, individu2, position):
    parent1 = individu1
    parent2 = individu2
    gen1 = []
    gen2 = []
    for i in range(0, position, 1):
        gen1.append(parent2[i])
        gen2.append(parent1[i])
    for i in range(position, 7, 1):
        gen1.append(parent1[i])
        gen2.append(parent2[i])
    init.append(gen1)
    init.append(gen2)


# pour faire mutation
def mutation(individu, position):  # position de la mutation
    if position < 2:
        individu[position] = random.choice(['1100', '0110', '0011'])
    else:
        individu[position] = random.choice(['1000', '0100', '0010', '0001'])
    return individu


# pour développer une génération
def developpement_generation(generation1, position_croisement, position_mutation):
    croisement_point(generation1, generation1[1], generation1[2], position_croisement)
    croisement_point(generation1, generation1[3], generation1[4], position_croisement)
    generation1.append(mutation(generation1[0], position_mutation))


# pour faire sélection
def selection(generation):
    # pour placer les éléments dans l'ordre décroissant
    generation.sort(reverse=True)
    generationfondue = []
    for i in range(len(generation)):
        generationfondue.append(generation[i])
    return generationfondue


def evaluation(generation):
    x = 0
    max = 0
    son = []
    for i in range(0, len(generation), 1):
        res = reser_maxi(intervalle, puissance(generation[i], capacite))
        if max < res:
            max = res
            x = i
    son.append(max)
    son.append(x)
    return son


def afficheGeneration(generation, nombreGeneration):
    print('Generation ', nombreGeneration, "\n")
    nombre = 1
    for i in generation:
        print(nombre, ') ', i, 'max_res: ', reser_maxi(intervalle, puissance(i, capacite)))
        nombre += 1
        print('\n')


nombre_generation = 1
# génération initiale
generation = createGeneration()
afficheGeneration(generation, nombre_generation)

evaluation_generation = evaluation(generation)
print('le meilleur individu est : ', generation[evaluation_generation[1]])
print('le meilleur score est :', evaluation_generation[0])

while nombre_generation < 3:
    developpement_generation(generation, 3, 2)
    generation = selection(generation)
    nombre_generation += 1
    afficheGeneration(generation, nombre_generation)
