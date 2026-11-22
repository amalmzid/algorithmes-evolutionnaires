# Grille de jetons (Algorithme génétique)

## Le problème

Sur une grille de **n × n** cases (ici n = 5), on place **k jetons** (ici k = 10) de façon que **chaque ligne et chaque colonne contienne un nombre pair de jetons**.

**Taille de l'espace de recherche :** on choisit les 10 cases qui reçoivent un jeton parmi 25 : C(25, 10) = **3 268 760** solutions.

---

## Algorithme génétique (**grille_jeton_genetique.py**)

- **Codage :** un individu est une liste de 25 valeurs 0 ou 1 (1 = jeton). La case (ligne, colonne) est à la position **ligne × n + colonne**. Chaque individu a exactement k jetons.
- **Fitness :** le nombre de lignes et de colonnes qui ont un nombre **impair** de jetons. On cherche le **minimum** (0 = solution faisable).
- **Sélection :** tournoi (on tire 3 individus, on garde le meilleur).
- **Croisement :** à 1 point, on échange la fin des deux parents (probabilité 0,9).
- **Réparation :** si un enfant n'a plus k jetons, on retire ou on ajoute des jetons au hasard.
- **Mutation :** on déplace un jeton vers une case vide (probabilité 0,3). Le nombre de jetons ne change pas.
- **Élitisme :** le meilleur individu est toujours gardé.
- Population de 70 individus, 300 générations au maximum. L'algorithme s'arrête dès que le score est 0.

## Résultat

Beaucoup de grilles sont faisables : une solution est trouvée en 0 à 7 générations. Si k est impair, il n'y a aucune solution.

![Exécution de grille_jeton_genetique.py](../capture/Capture%20d'%C3%A9cran%202026-11-22%20202105.png)

**Interprétation :** le score est 0 dès la génération 0, donc une solution faisable existe déjà dans la population de départ. Les 10 jetons sont répartis avec 2 jetons par ligne et 2, 2, 0, 2, 4 par colonne : tous ces nombres sont pairs.
