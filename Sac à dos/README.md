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

## Recuit simulé (**sacàdos_recuit_simule.py**)

On travaille sur **une seule solution**. À chaque étape, on inverse **un objet au hasard** (le sac doit rester valide).
- Voisin **meilleur ou égal** : toujours accepté.
- Voisin **moins bon** : accepté avec la probabilité **exp(delta / T)**.
- La température baisse à chaque étape (**T = alpha × T**, avec 3000 itérations, T0 = 10 et alpha = 0,999).

## Recherche tabou (**sacàdos_tabu.py**)

On travaille aussi sur **une seule solution**. À chaque étape :
1. on génère 4 voisins (un objet inversé chacun) ;
2. on enlève les voisins **tabous** (déjà visités récemment) et ceux qui dépassent la capacité ;
3. on va vers le **meilleur voisin**, même s'il est moins bon ;
4. on l'ajoute à la **liste tabou** (qui garde les 2 dernières solutions).

---

## Comparaison

| | Génétique | Recuit simulé | Tabou |
|---|---|---|---|
| Solutions en même temps | 70 | 1 | 1 |
| Voisins regardés à chaque étape | (croisement et mutation) | 1, au hasard | 4, au hasard |
| Comment sortir d'un minimum local | croisement et mutation | hasard + température | liste tabou (mémoire) |
