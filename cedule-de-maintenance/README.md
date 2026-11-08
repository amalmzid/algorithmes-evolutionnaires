# TD1 - Cédule de maintenance par algorithme génétique

## Le problème

**7 centrales** doivent être arrêtées pour maintenance pendant l'année (**4 périodes**).
On cherche **quand arrêter chaque centrale** pour garder **le plus d'électricité en réserve**.

| Centrale | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Puissance (MW) | 20 | 15 | 35 | 40 | 15 | 15 | 10 |
| Durée de maintenance | 2 | 2 | 1 | 1 | 1 | 1 | 1 |

- Puissance totale : **150 MW**
- Besoin des 4 périodes : **80, 90, 65, 70 MW**

---

## La formulation

**Réserve = 150 - (puissance des centrales arrêtées) - besoin**

- **Règles :** une centrale de 2 périodes s'arrête 2 périodes **qui se suivent**, et la réserve doit être **≥ 0**.
- **Fonction objectif :** **maximiser la plus petite réserve** des 4 périodes.

**fitness = min(R1, R2, R3, R4)** (0 si une réserve est négative)

Une cédule est aussi sûre que **sa pire période**.

---

## L'encodage

Chaque centrale = **un code de 4 chiffres** (**1** = arrêtée, **0** = marche).

- Centrales 1 et 2 : **1100**, **0110**, **0011**
- Centrales 3 à 7 : **1000**, **0100**, **0010**, **0001**

Une solution = 7 codes : **0110 0011 0001 1000 0100 0010 1000** → réserves **20, 25, 35, 30** → fitness **20**

---

## L'algorithme génétique

42 solutions, 20 générations, croisement 80 %, mutation 20 %.

1. **Élitisme :** la meilleure solution passe directement.
2. **Sélection par loterie :** plus la fitness est grande, plus on a de billets.
3. **Croisement :** on coupe 2 parents et on échange les fins.
4. **Mutation par inversion :** on retourne un morceau du code (**0001** → **0100**). Si le code devient impossible, on garde l'ancien.
5. **Mutation par remplacement** (testée en plus) : on remplace le code par un autre code possible.

On travaille toujours sur des **codes entiers de 4 chiffres**, pour ne jamais créer une cédule impossible.

---

## Résultats

### Mutation par inversion
![Mutation par inversion](../capture/Capture%20d'%C3%A9cran%202026-11-08%20220526.png)

### Mutation par remplacement
![Mutation par remplacement et résultats](../capture/Capture%20d'%C3%A9cran%202026-11-08%20220549.png)

- Les deux mutations trouvent une fitness de **25**, la **meilleure valeur possible** (vérifié sur les 9 216 solutions).
- Elles trouvent des solutions **différentes**, car 43 solutions donnent 25.
- Grâce à l'élitisme, la meilleure fitness **ne baisse jamais**.

