# Cédule de maintenance (Génétique, Recuit simulé, Recherche tabou)

7 centrales électriques doivent être arrêtées pour maintenance pendant l'année (4 périodes). Il faut choisir **quand arrêter chaque centrale** pour garder le plus d'électricité en réserve.

- **Codage :** une solution est une liste de 7 codes de 4 chiffres (1 = arrêtée, 0 = marche). Centrales 1 et 2 : **1100**, **0110**, **0011**. Centrales 3 à 7 : **1000**, **0100**, **0010**, **0001**.
- **Score :** **min(R1, R2, R3, R4)**, avec **Réserve = 150 - (puissance arrêtée) - besoin**. On cherche le **maximum** (0 si une réserve est négative).
- Le meilleur score possible est **25**.

---

## Algorithme génétique (**ordonance_genetique.py**)

On garde une **population** de cédules qui évolue de génération en génération.
- **Croisement :** on coupe 2 parents et on échange les fins (par blocs de 4 chiffres).
- **Mutation :** on remplace le code d'une centrale par un autre code possible.
- **Sélection :** on trie les individus et on garde les meilleurs.

On travaille toujours sur des **codes entiers de 4 chiffres** pour ne jamais créer une cédule impossible.

![Mutation par inversion](../capture/Capture%20d'%C3%A9cran%202026-11-08%20220526.png)
![Mutation par remplacement](../capture/Capture%20d'%C3%A9cran%202026-11-08%20220549.png)

## Recuit simulé (**ordonance_recuit_simule.py**)

On travaille sur **une seule cédule**. À chaque étape, on change **le code d'une centrale au hasard**.
- Voisin **meilleur ou égal** : toujours accepté.
- Voisin **moins bon** : accepté avec la probabilité **exp(delta / T)**.
- La température baisse à chaque palier (**T = alpha × T**, avec T0 = 50, alpha = 0,9, 10 itérations par palier).

## Recherche tabou (**ordonance_tabou.py**)

On travaille aussi sur **une seule cédule**. À chaque itération :
1. on génère les **19 voisins** (une centrale change de code) ;
2. on enlève les voisins **tabous** (déjà visités récemment) ;
3. on va vers le voisin avec la **meilleure réserve minimale**, même s'il est moins bon ;
4. on l'ajoute à la **liste tabou** (qui garde les 10 dernières cédules, 100 itérations).

---

## Comparaison

| | Génétique | Recuit simulé | Tabou |
|---|---|---|---|
| Solutions en même temps | plusieurs | 1 | 1 |
| Voisins regardés à chaque étape | (croisement et mutation) | 1, au hasard | tous (19) |
| Comment sortir d'un minimum local | croisement et mutation | hasard + température | liste tabou (mémoire) |
