import random
from collections import deque

# Une solution est une liste de 0 et de 1, un element par objet :
# 1 = l'objet est dans le sac, 0 = il n'y est pas. Ex: [1, 0, 1, 0, 0] -> objets 0 et 2 pris


def calculer_poids_total(solut, poids):
    # additionne le poids de tous les objets pris (element = 1)
    pt = 0
    for i in range(len(solut)):
        if solut[i] == 1:
            pt += poids[i]
    return pt


def calculer_valeur_totale(solut, valeurs):
    # additionne la valeur de tous les objets pris (element = 1)
    vt = 0
    for i in range(len(solut)):
        if solut[i] == 1:
            vt += valeurs[i]
    return vt


def generer_voisins(solut, nbr_voisinage):
    # Un voisin = on inverse un objet (pris <-> non pris) ; on en génère nbr_voisinage, à des positions au hasard
    v = []
    # random.sample choisit nbr_voisinage positions differentes
    for i in random.sample(range(len(solut)), nbr_voisinage):
        voisin = solut[:]          # copie pour ne pas modifier la solution actuelle
        voisin[i] = 1 - voisin[i]  # 0 devient 1 et 1 devient 0
        v.append(voisin)
    return v


def tabu_search(valeurs, capacite, poids, nbr_iter, taille_tabu, solut_depart, nbr_voisinage, tabu_initial):
    # on part de la solution de depart, qui est aussi la meilleure connue au debut
    solution_actuelle = solut_depart[:]
    meilleur_solut = solution_actuelle[:]
    meilleur_valeur = calculer_valeur_totale(solution_actuelle, valeurs)

    # liste tabou : memoire des dernieres solutions visitees (interdites pour eviter de tourner en rond)
    # deque(maxlen=...) oublie automatiquement la plus ancienne quand elle est pleine
    tabu_list = deque(maxlen=taille_tabu)
    tabu_list.extend(tabu_initial)

    for i in range(nbr_iter):
        # 1. on genere des voisins de la solution actuelle
        v = generer_voisins(solution_actuelle, nbr_voisinage)
        # 2. on elimine les voisins tabous et ceux qui depassent la capacite du sac
        v = [voisin for voisin in v if voisin not in tabu_list and calculer_poids_total(voisin, poids) <= capacite]

        # plus aucun voisin possible : on arrete la recherche
        if not v:
            break

        # 3. on se deplace vers le meilleur voisin (meme s'il est moins bon que la solution actuelle)
        solution_actuelle = max(v, key=lambda x: calculer_valeur_totale(x, valeurs))
        valeur_actuelle = calculer_valeur_totale(solution_actuelle, valeurs)

        # 4. on ajoute cette solution a la liste tabou
        tabu_list.append(solution_actuelle)

        # 5. on garde la meilleure solution rencontree depuis le debut
        if valeur_actuelle > meilleur_valeur:
            meilleur_solut = solution_actuelle[:]
            meilleur_valeur = valeur_actuelle

    return meilleur_solut, meilleur_valeur


# valeurs[i] et poids[i] : valeur et poids de l'objet i
valeurs = [10, 5, 15, 7, 6, 18, 3, 12, 9, 8]
poids = [2, 3, 5, 7, 1, 4, 1, 6, 3, 2]
capacite = 15  # poids maximal que le sac peut contenir

solut_depart = [1, 0, 0, 0, 1, 0, 1, 0, 0, 0]  # solution de depart
tabu_initial = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 1, 0, 1, 0, 0, 0]]  # solutions deja interdites au depart

nbr_iter = 200      # nombre d'iterations
taille_tabu = 2     # nombre de solutions gardees en memoire dans la liste tabou
nbr_voisinage = 4   # nombre de voisins generes a chaque iteration

meilleur_solut, meilleur_valeur = tabu_search(valeurs, capacite, poids, nbr_iter, taille_tabu,
                                              solut_depart, nbr_voisinage, tabu_initial)

print("Meilleure solution trouvée (Tabu Search):", meilleur_solut)
print("Valeur maximale:", meilleur_valeur)
print("Poids total:", calculer_poids_total(meilleur_solut, poids))
