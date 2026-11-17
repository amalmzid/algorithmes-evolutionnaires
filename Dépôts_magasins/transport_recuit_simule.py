import math
import random

# Données du problème
#                    M1  M2  M3
matrice_couts = [[5,  3,  4],    # D1
                 [6,  7,  2]]    # D2

offres = [8, 9]          # containers disponibles dans D1, D2
demandes = [4, 5, 8]     # containers commandes par M1, M2, M3


# Fonctions

def calculer_cout_total(solution, matrice_couts):
    # Calculer le cout total : somme de (cout x quantite) pour chaque case
    cout_total = 0
    for i in range(len(solution)):            # pour chaque depot
        for j in range(len(solution[i])):     # pour chaque magasin
            cout_total += matrice_couts[i][j] * solution[i][j]
    return cout_total


def generer_solution_initiale(offres, demandes):
    # Generer une solution aleatoire qui respecte les offres et les demandes.
    reste_offre = offres[:]
    reste_demande = demandes[:]
    solution = [[0] * len(demandes) for _ in range(len(offres))]

    cases = [(i, j) for i in range(len(offres)) for j in range(len(demandes))]
    random.shuffle(cases)

    for i, j in cases:
        quantite = min(reste_offre[i], reste_demande[j])
        solution[i][j] = quantite
        reste_offre[i] -= quantite
        reste_demande[j] -= quantite
    return solution


def generer_voisin(solution):
    # Un voisin = on deplace 1 container :
    #   le depot i envoie 1 de moins au magasin j et 1 de plus au magasin l
    #   le depot k fait l'inverse (1 de plus a j, 1 de moins a l)
    voisins = []
    for i in range(len(solution)):
        for k in range(i + 1, len(solution)):
            for j in range(len(solution[0])):
                for l in range(len(solution[0])):
                    if j != l and solution[i][j] > 0 and solution[k][l] > 0:
                        voisin = [ligne[:] for ligne in solution]   # copie
                        voisin[i][j] -= 1
                        voisin[i][l] += 1
                        voisin[k][j] += 1
                        voisin[k][l] -= 1
                        voisins.append(voisin)
    # on choisit un voisin au hasard
    return random.choice(voisins) if voisins else solution


def recuit_simule(matrice_couts, offres, demandes, temperature_initiale, temperature_finale,
                  alpha, iterations_par_palier):
    # Solution de depart aleatoire
    solution_actuelle = generer_solution_initiale(offres, demandes)
    cout_actuel = calculer_cout_total(solution_actuelle, matrice_couts)

    meilleure_solution = [ligne[:] for ligne in solution_actuelle]
    meilleur_cout = cout_actuel

    temperature = temperature_initiale

    while temperature > temperature_finale:
        for _ in range(iterations_par_palier):
            voisin = generer_voisin(solution_actuelle)
            cout_voisin = calculer_cout_total(voisin, matrice_couts)
            delta = cout_voisin - cout_actuel

            # Voisin meilleur : toujours accepte
            # Voisin moins bon : accepte avec la probabilite exp(-delta / T)
            if delta <= 0 or random.random() < math.exp(-delta / temperature):
                solution_actuelle = voisin
                cout_actuel = cout_voisin

                # Mettre a jour la meilleure solution
                if cout_actuel < meilleur_cout:
                    meilleure_solution = [ligne[:] for ligne in solution_actuelle]
                    meilleur_cout = cout_actuel

        # Refroidissement
        temperature *= alpha

    return meilleure_solution, meilleur_cout


# Execution
temperature_initiale = 20
temperature_finale = 0.1
alpha = 0.9
iterations_par_palier = 10

meilleure_solution, meilleur_cout = recuit_simule(matrice_couts, offres, demandes, temperature_initiale,
                                                  temperature_finale, alpha, iterations_par_palier)

print("Meilleure solution :", meilleure_solution)
print("Cout minimal :", meilleur_cout)
