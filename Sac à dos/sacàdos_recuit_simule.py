import math
import random

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


def generer_voisin(solut, poids, capacite):
    # Un voisin = on inverse un objet au hasard (pris <-> non pris)
    # on recommence tant que le sac depasse la capacite
    while True:
        voisin = solut[:]          # copie pour ne pas modifier la solution actuelle
        i = random.randint(0, len(solut) - 1)
        voisin[i] = 1 - voisin[i]  # 0 devient 1 et 1 devient 0
        if calculer_poids_total(voisin, poids) <= capacite:
            return voisin


def recuit_simule(valeurs, capacite, poids, solut_depart, nbr_iter, temperature, alpha):
    # on part de la solution de depart, qui est aussi la meilleure connue au debut
    solution_actuelle = solut_depart[:]
    valeur_actuelle = calculer_valeur_totale(solution_actuelle, valeurs)
    meilleur_solut = solution_actuelle[:]
    meilleur_valeur = valeur_actuelle

    for i in range(nbr_iter):
        # 1. on genere un voisin au hasard
        voisin = generer_voisin(solution_actuelle, poids, capacite)
        valeur_voisin = calculer_valeur_totale(voisin, valeurs)
        delta = valeur_voisin - valeur_actuelle

        # 2. voisin meilleur (ou egal) : accepte
        #    voisin moins bon : accepte avec la probabilite exp(delta / T)
        if delta >= 0 or random.random() < math.exp(delta / temperature):
            solution_actuelle = voisin
            valeur_actuelle = valeur_voisin

            # 3. on garde la meilleure solution rencontree depuis le debut
            if valeur_actuelle > meilleur_valeur:
                meilleur_solut = solution_actuelle[:]
                meilleur_valeur = valeur_actuelle

        # 4. refroidissement : la temperature diminue a chaque iteration
        temperature = alpha * temperature

    return meilleur_solut, meilleur_valeur


# valeurs[i] et poids[i] : valeur et poids de l'objet i
valeurs = [10, 5, 15, 7, 6, 18, 3, 12, 9, 8]
poids = [2, 3, 5, 7, 1, 4, 1, 6, 3, 2]
capacite = 15  # poids maximal que le sac peut contenir

solut_depart = [1, 0, 0, 0, 1, 0, 1, 0, 0, 0]  # solution de depart

nbr_iter = 3000              # nombre d'iterations
temperature_initiale = 10    # temperature de depart
alpha = 0.999                # coefficient de refroidissement

meilleur_solut, meilleur_valeur = recuit_simule(valeurs, capacite, poids, solut_depart,
                                                nbr_iter, temperature_initiale, alpha)

print("Meilleure solution trouvée (Recuit simulé):", meilleur_solut)
print("Valeur maximale:", meilleur_valeur)
print("Poids total:", calculer_poids_total(meilleur_solut, poids))
