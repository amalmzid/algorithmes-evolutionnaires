import random
from collections import deque

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


def generer_voisins(solution):
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
    return voisins


def tabu_search(matrice_couts, offres, demandes, nombre_iterations, taille_tabu):
    # Solution de depart aleatoire
    solution_actuelle = generer_solution_initiale(offres, demandes)

    meilleure_solution = [ligne[:] for ligne in solution_actuelle]
    meilleur_cout = calculer_cout_total(solution_actuelle, matrice_couts)
    print("Solution initiale :", solution_actuelle, " cout =", meilleur_cout)

    # Liste tabou
    tabu_list = deque(maxlen=taille_tabu)
    tabu_list.append(solution_actuelle)

    for iteration in range(1, nombre_iterations + 1):
        # Generer les voisins et enlever ceux qui sont tabous
        voisins = generer_voisins(solution_actuelle)
        voisins = [voisin for voisin in voisins if voisin not in tabu_list]

        # aucun voisin autorise donc on arrete
        if not voisins:
            print("Plus de voisin autorise -> arret")
            break

        # Aller vers le meilleur voisin meme s'il est moins bon 
        solution_actuelle = min(voisins, key=lambda x: calculer_cout_total(x, matrice_couts))
        cout_actuel = calculer_cout_total(solution_actuelle, matrice_couts)

        # Ajouter la solution a la liste tabou
        tabu_list.append(solution_actuelle)

        # Mettre a jour la meilleure solution
        if cout_actuel < meilleur_cout:
            meilleure_solution = [ligne[:] for ligne in solution_actuelle]
            meilleur_cout = cout_actuel

        print(f"Iteration {iteration:2d} : {solution_actuelle}  cout = {cout_actuel}"
              f"  | meilleur = {meilleur_cout}")

    return meilleure_solution, meilleur_cout


# Execution
nombre_iterations = 20
taille_tabu = 10

meilleure_solution, meilleur_cout = tabu_search(matrice_couts, offres, demandes,
                                                nombre_iterations, taille_tabu)

print("\nMeilleure solution trouvee (Tabu Search):")
print("        M1  M2  M3")
print(f"  D1  {meilleure_solution[0][0]:3d} {meilleure_solution[0][1]:3d} {meilleure_solution[0][2]:3d}")
print(f"  D2  {meilleure_solution[1][0]:3d} {meilleure_solution[1][1]:3d} {meilleure_solution[1][2]:3d}")
print("Cout minimal:", meilleur_cout)
