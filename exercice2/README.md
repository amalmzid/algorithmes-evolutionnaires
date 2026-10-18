# TD1 - Exercice 2 : Problème de transport (Branch and Bound + Recherche tabou)


## 1. Le problème

Une entreprise possède **2 dépôts** (D1, D2) remplis de containers.
**3 magasins** (M1, M2, M3) commandent des containers.
Chaque container transporté coûte de l'argent, selon le trajet :

| Coût d'un container | M1 | M2 | M3 | Containers dans le dépôt |
|---|---|---|---|---|
| **D1** | 5 | 3 | 4 | **8** |
| **D2** | 6 | 7 | 2 | **9** |
| **Commandé par le magasin** | **4** | **5** | **8** | |

**Question :** combien de containers chaque dépôt doit-il envoyer à chaque magasin pour que le **coût total soit le plus petit possible** ?

Offre = 8 + 9 = **17** et demande = 4 + 5 + 8 = **17**.
Elles sont égales, donc le problème est **équilibré** : tous les containers sont envoyés et chaque magasin est entièrement servi.

---

## 2. Le modèle mathématique

**Variables :** `x_ij` = nombre de containers envoyés du dépôt `i` au magasin `j`.
Ce sont des **nombres entiers ≥ 0** (on ne peut pas envoyer 2,5 containers).

**Objectif (minimiser le coût total) :**
```
Z = 5·x11 + 3·x12 + 4·x13 + 6·x21 + 7·x22 + 2·x23
```

**Contraintes :**
```
x11 + x12 + x13 = 8      D1 envoie tous ses containers
x21 + x22 + x23 = 9      D2 envoie tous ses containers
x11 + x21       = 4      M1 reçoit ce qu'il a commandé
x12 + x22       = 5      M2 reçoit ce qu'il a commandé
x13 + x23       = 8      M3 reçoit ce qu'il a commandé
x_ij >= 0 et entier
```

---

## 3. Solution 1 (Branch and Bound)

### 3.1 L'idée

1. **Relaxation :** on résout le problème **en autorisant les nombres à virgule** (x = 2,5 est accepté).
   Sans la règle « entier », cela devient un programme linéaire normal, facile à résoudre.
2. **Si une valeur a des décimales** (par exemple `x11 = 2,5`), on coupe le problème en deux :
   - branche gauche : on ajoute `x11 <= 2`
   - branche droite : on ajoute `x11 >= 3`

3. **Évaluation (bound) :** le coût du problème relaxé est **le meilleur coût que cette branche peut atteindre**.
   S'il n'est pas meilleur qu'une solution entière déjà trouvée, on **coupe** la branche.
4. On recommence jusqu'à ce que chaque branche soit coupée ou donne une solution entière.
   La meilleure solution entière est l'optimum.

```
                Noeud 0 : x11 = 2,5, Z = 50,5
               /                          \
    Noeud 1 : on ajoute x11 <= 2     Noeud 2 : on ajoute x11 >= 3
    on résout à nouveau              on résout à nouveau
```



### 3.3 Le code (branch_and_bound.py)

Le problème est donné à la fonction `linprog` de SciPy :

```python
linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
```

| Argument | Rôle | Valeur |
|---|---|---|
| `c` | coût de chaque trajet, c'est-à-dire **ce qu'on minimise** | `[5, 3, 4, 6, 7, 2]` |
| `A_eq` | **partie gauche des contraintes** : une ligne par contrainte, une colonne par variable (1 = la variable est dans la contrainte) | matrice 5 × 6 |
| `b_eq` | **partie droite des contraintes** : la valeur que chaque contrainte doit atteindre | `[8, 9, 4, 5, 8]` |
| `bounds` | min et max de chaque variable. **C'est ce que la séparation modifie** | `[(0, None)] * 6` |
| `method` | algorithme du solveur (HiGHS, un simplexe rapide) | `"highs"` |

En une phrase : **minimiser `c·x` tel que `A_eq·x = b_eq` et chaque `x` reste dans ses bornes.**

Lecture de la matrice `A_eq` :
```
         x11 x12 x13 x21 x22 x23
D1    [   1,  1,  1,  0,  0,  0 ]   ->  x11 + x12 + x13 = 8
D2    [   0,  0,  0,  1,  1,  1 ]   ->  x21 + x22 + x23 = 9
M1    [   1,  0,  0,  1,  0,  0 ]   ->  x11 + x21       = 4
M2    [   0,  1,  0,  0,  1,  0 ]   ->  x12 + x22       = 5
M3    [   0,  0,  1,  0,  0,  1 ]   ->  x13 + x23       = 8
```

Ce que renvoie `linprog` :

| Champ | Signification | Notre résultat |
|---|---|---|
| `result.x` | valeurs des variables | `[3, 5, 0, 1, 0, 8]` |
| `result.fun` | **valeur de la fonction objectif** = coût = `c · x` | `52.0` |
| `result.success` | `True` si une solution existe | `True` |

Vérification : `result.fun = 5·3 + 3·5 + 4·0 + 6·1 + 7·0 + 2·8 = 52`.
Dans Branch and Bound, `result.fun` est la **borne** : le coût le plus bas que le noeud peut atteindre.

Étapes de la boucle principale :
- **A.** résoudre le problème relaxé
- **B.** pas de solution ? on coupe la branche
- **C. Évaluation :** coût >= meilleur coût trouvé ? on coupe la branche
- **D.** toutes les valeurs sont entières ? nouvelle meilleure solution
- **E. Séparation :** une valeur comme 2,5 ? on crée deux noeuds, `x <= 2` et `x >= 3`

### 3.4 Résultat affiché

![Exécution de branch_and_bound.py](../capture/branch-and-bound-run.png)

Le premier problème relaxé donne déjà une solution entière : un seul noeud, coût minimal **52**.

---

## 4. Solution 2 (Recherche tabou)

### 4.1 L'idée  

1. On part d'une **solution valide aléatoire**.
2. À chaque itération :
   - on liste tous les **voisins** (solutions obtenues avec un petit changement)
   - on enlève les voisins qui sont dans la **liste tabou** (déjà visités récemment)
   - on va vers le **voisin le moins cher qui reste, même s'il est moins bon**
   - on l'ajoute à la liste tabou
   - si c'est la meilleure solution jamais vue, on la garde en mémoire
3. On s'arrête après `nombre_iterations`, ou quand tous les voisins sont tabous.

Aller vers une solution moins bonne paraît étrange, mais c'est la force de la méthode :
elle permet de **sortir des minimums locaux** au lieu de rester bloquée.
La liste tabou l'empêche de revenir directement en arrière.


### 4.2 Les fonctions

| Fonction | Rôle |
|---|---|
| `calculer_cout_total` | additionne `coût × quantité` pour chaque case |
| `generer_solution_initiale` | crée une solution de départ aléatoire mais valide |
| `generer_voisins` | liste toutes les solutions obtenues en déplaçant 1 container |
| `tabu_search` | boucle principale : choisit le meilleur voisin non tabou |



#### `generer_voisins`
Un mouvement déplace 1 container entre 2 dépôts (i, k) et 2 magasins (j, l) :
```
              magasin j   magasin l
dépôt i          -1          +1
dépôt k          +1          -1
```
Les totaux des lignes et des colonnes ne changent pas, donc le voisin reste valide.
Le mouvement n'est possible que si `j != l` et si les cases qui perdent 1 sont `> 0`.

Exemple : les voisins de `[[3,5,0],[1,0,8]]` (coût 52) sont

| Mouvement de D1 | Voisin | Coût |
|---|---|---|
| M1 → M3 | `[[2,5,1],[2,0,7]]` | 55 |
| M2 → M1 | `[[4,4,0],[0,1,8]]` | 55 |
| M2 → M3 | `[[3,4,1],[1,1,7]]` | 58 |

Tous coûtent plus que 52, donc 52 est un minimum.

#### `tabu_search`
```python
voisins = [voisin for voisin in voisins if voisin not in tabu_list]
solution_actuelle = min(voisins, key=lambda x: calculer_cout_total(x, matrice_couts))
```
On enlève les voisins tabous, puis on prend celui qui a le **coût le plus bas**,
même s'il est moins bon que la solution actuelle.

### 4.3 Paramètres

En bas de `tabu_transport.py` :
```python
nombre_iterations = 20   # nombre d'itérations
taille_tabu = 10         # nombre de solutions récentes interdites
```

### 4.4 Exécution


![Exécution de tabu_transport.py](../capture/tabu-run.png)

---

## 5. Comparaison

| | Branch and Bound | Recherche tabou |
|---|---|---|
| Type | exacte | métaheuristique |
| Garantit l'optimum ? | **oui** | non (mais le trouve très souvent) |
| Aléatoire ? | non, toujours le même résultat | oui, la solution de départ est aléatoire |
| Gros problèmes | peut devenir très lent (arbre énorme) | reste rapide |
| Sur cet exercice | 1 noeud, coût 52 | coût 52 en quelques itérations |
