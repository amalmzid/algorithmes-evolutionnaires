# Transport de containers (Génétique, Recuit simulé, Recherche tabou)

2 dépôts (D1 : 8 containers, D2 : 9 containers) livrent 3 magasins (M1 : 4, M2 : 5, M3 : 8).
Chaque trajet a un coût par container. Il faut trouver combien de containers envoyer de chaque dépôt à chaque magasin pour que le **coût total soit le plus petit**.
Une solution est une matrice **[[x11, x12, x13], [x21, x22, x23]]**. Le meilleur coût est **52**.

---

## Algorithme génétique (**transport_genetique.py**)

Écrit comme **ordonance_genetique.py**. On garde une **population** de 5 individus qui évolue pendant 30 générations.
- **Codage :** un individu est l'**ordre de remplissage** des 6 cases (dépôt, magasin). Chaque case reçoit le maximum possible, donc la solution respecte toujours les offres et les demandes.
- **Croisement :** on garde le début d'un parent, puis on complète dans l'ordre de l'autre parent (sans doublon).
- **Mutation :** on échange 2 cases dans l'ordre.
- **Sélection :** on trie par coût et on garde les meilleurs.

![Exécution de l'algorithme génétique](../capture/Capture%20d'%C3%A9cran%202026-11-22%20203202.png)

**Interprétation :** l'algorithme génétique trouve un coût minimal de **52**. D1 envoie 3, 5 et 0 containers à M1, M2 et M3, et D2 envoie 1, 0 et 8 (3×5 + 5×3 + 1×6 + 8×2 = 52). Les offres (8 et 9) et les demandes (4, 5 et 8) sont bien respectées.

## Recuit simulé (**transport_recuit_simule.py**)

On travaille sur **une seule solution**. À chaque étape, on tire **un voisin au hasard**.
- Voisin **moins cher ou égal** : toujours accepté.
- Voisin **plus cher** : accepté avec la probabilité **exp(-delta / T)**.
- La température baisse à chaque palier (**T = alpha × T**, avec T0 = 20 et alpha = 0,9).

![Exécution du recuit simulé](../capture/Capture%20d'%C3%A9cran%202026-11-22%20203208.png)

**Interprétation :** le recuit simulé trouve la même solution que le génétique, avec le même coût minimal de **52**. Il y arrive en acceptant parfois des solutions plus chères au début, quand la température est élevée.

## Recherche tabou (**transport_tabu.py**)

On travaille aussi sur **une seule solution**. On part d'une solution valide aléatoire. À chaque itération :
1. on génère **tous les voisins** ;
2. on enlève les voisins **tabous** (déjà visités récemment) ;
3. on va vers le **voisin le moins cher**, même s'il est moins bon ;
4. on l'ajoute à la **liste tabou** (qui garde les 10 dernières solutions).

![Exécution de la recherche tabou](../capture/tabu-run.png)

**Interprétation :** le coût baisse de 79 (solution de départ) à **52** en 5 itérations. Ensuite, la recherche tabou continue vers le meilleur voisin autorisé, même s'il est plus cher (55, 58, 61...), mais le meilleur coût reste 52. C'est la solution finale, la même que celle des deux autres méthodes.

**Voisin (recuit et tabou) :** on déplace 1 container entre 2 dépôts et 2 magasins. Les totaux des lignes et des colonnes ne changent pas, donc le voisin reste valide.
```
              magasin j   magasin l
dépôt i          -1          +1
dépôt k          +1          -1
```

