# Sac à dos (Génétique, Recuit simulé, Recherche tabou)

10 objets, chacun avec une **valeur** et un **poids**. Le sac supporte au maximum **15** de poids. Il faut choisir les objets pour que la **valeur totale soit la plus grande**.
Une solution est une liste de 0 et de 1 (1 = objet pris) : **[1, 0, 1, 0, 1, 1, 1, 0, 0, 1]**. Le meilleur résultat est une valeur de **60** pour un poids de 15.

---

## Algorithme génétique (**sacàdos_genetique.py**)

On garde une **population** de 70 solutions qui évolue pendant 200 générations.
- **Sélection :** tournoi (on tire 3 solutions, on garde la meilleure).
- **Croisement :** on coupe 2 parents et on échange les fins (probabilité 0,9).
- **Mutation :** on inverse un objet (pris <-> non pris) (probabilité 0,3).
- **Réparation :** si le sac est trop lourd, on retire des objets au hasard.
- **Élitisme :** la meilleure solution trouvée est toujours gardée.

![Exécution de l'algorithme génétique](../capture/Capture%20d'%C3%A9cran%202026-11-22%20202851.png)

**Interprétation :** dès la génération 20, la meilleure valeur est déjà **60** et elle ne change plus jusqu'à la génération 200. Le sac choisi contient les objets 1, 3, 5, 6, 7 et 10 (valeur 10 + 15 + 6 + 18 + 3 + 8 = 60) pour un poids de **15**, donc la capacité est respectée et utilisée en entier.

## Recuit simulé (**sacàdos_recuit_simule.py**)

On travaille sur **une seule solution**. À chaque étape, on inverse **un objet au hasard** (le sac doit rester valide).
- Voisin **meilleur ou égal** : toujours accepté.
- Voisin **moins bon** : accepté avec la probabilité **exp(delta / T)**.
- La température baisse à chaque étape (**T = alpha × T**, avec 3000 itérations, T0 = 10 et alpha = 0,999).

![Exécution du recuit simulé](../capture/Capture%20d'%C3%A9cran%202026-11-22%20202947.png)

**Interprétation :** le recuit simulé trouve la même solution que le génétique, de valeur **60** et de poids **15**. Au début, la température élevée lui permet d'accepter des solutions moins bonnes pour explorer. Ensuite, elle baisse et l'algorithme se stabilise sur la meilleure solution.

## Recherche tabou (**sacàdos_tabu.py**)

On travaille aussi sur **une seule solution**. À chaque étape :
1. on génère 4 voisins (un objet inversé chacun) ;
2. on enlève les voisins **tabous** (déjà visités récemment) et ceux qui dépassent la capacité ;
3. on va vers le **meilleur voisin**, même s'il est moins bon ;
4. on l'ajoute à la **liste tabou** (qui garde les 2 dernières solutions).

![Exécution de la recherche tabou](../capture/Capture%20d'%C3%A9cran%202026-11-22%20202953.png)

**Interprétation :** la recherche tabou trouve aussi la solution de valeur **60** et de poids **15**, la même que les deux autres méthodes. Les trois méthodes arrivent donc au même résultat, qui est le meilleur possible pour ce sac.

