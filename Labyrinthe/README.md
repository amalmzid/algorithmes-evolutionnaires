# Labyrinthe (Algorithme génétique)

## Le problème

Un robot se déplace dans un labyrinthe de 10 × 10 cases. L'entrée est la case (1,1) en haut à gauche, la sortie est la case (10,10) en bas à droite.
Le robot s'arrête quand il **se cogne contre un mur**, **revient sur une case déjà visitée** ou **atteint la sortie**.
Il faut trouver un parcours qui mène à la sortie.

La grille (1 = mur, 0 = case libre) est écrite à la main dans **labyrinthe_genetique.py**. À vérifier avec l'énoncé.

---

## Algorithme génétique (**labyrinthe_genetique.py**)

- **Codage :** un individu est une liste de **40 déplacements** (0 = haut, 1 = bas, 2 = gauche, 3 = droite).
- **Fitness :** on fait marcher le robot. On calcule le **nombre de déplacements qui restent** entre sa dernière case et la sortie (0 = sortie atteinte). On cherche le **minimum**.
  Cette distance est calculée dans le labyrinthe (parcours en largeur depuis la sortie) et non à vol d'oiseau, sinon le robot reste bloqué dans les impasses.
- **Sélection :** tournoi (on tire 3 individus, on garde le meilleur).
- **Croisement :** à 1 point, on échange la fin des deux parents (probabilité 0,9).
- **Mutation :** un déplacement est remplacé par une autre direction (probabilité 0,3).
- **Élitisme :** le meilleur individu est toujours gardé.
- Population de 70 individus, 300 générations au maximum. L'algorithme s'arrête dès que la sortie est atteinte.

## Résultat

Le robot atteint la sortie en 18 déplacements (le minimum) ou 20, en moins de 200 générations.

Exécution : **python labyrinthe_genetique.py**.
