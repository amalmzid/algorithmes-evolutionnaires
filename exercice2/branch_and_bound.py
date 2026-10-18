import math
from scipy.optimize import linprog

# Données du problème
COST = [[5,  3,  4],   # D1
        [6,  7,  2]]   # D2

SUPPLY = [8, 9]        # containers disponibles dans D1, D2
DEMAND = [4, 5, 8]     # containers commandes par M1, M2, M3


NAMES = ["x11", "x12", "x13", "x21", "x22", "x23"]


c = COST[0] + COST[1]

# contraintes

#          x11 x12 x13 x21 x22 x23
A_eq = [[1,  1,  1,  0,  0,  0],   # D1 envoie tout = 8
        [0,  0,  0,  1,  1,  1],   # D2 envoie tout = 9
        [1,  0,  0,  1,  0,  0],   # M1 recoit tout = 4
        [0,  1,  0,  0,  1,  0],   # M2 recoit tout = 5
        [0,  0,  1,  0,  0,  1]]   # M3 recoit tout = 8
        
b_eq = SUPPLY + DEMAND


# Fonctions 

def solve_relaxation(bounds):
    """Solve the problem WITHOUT the 'integer' rule (decimals allowed).
    bounds = list of (min, max) for each variable.
    Returns the result of linprog."""
    return linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

def find_fractional_variable(x):
    """Return the index of the first variable that is NOT a whole number.
    Return None if all variables are whole numbers."""
    for i in range(len(x)):
        if abs(x[i] - round(x[i])) > 1e-6:
            return i
    return None

def branch_and_bound():
    best_cost = math.inf     
    best_x = None          

    # liste des noeuds à explorer
    root = [(0, None)] * 6
    nodes_to_explore = [root]
    node_number = 0

    while nodes_to_explore:
        bounds = nodes_to_explore.pop()   # take one node from the list
        node_number += 1
        print(f"\nNode {node_number}: bounds = {bounds}")

        # etape A: resolution du probleme relache
        result = solve_relaxation(bounds)

        # etape B: couper cette branche s'il n'y a pas de solution
        if not result.success:
            print("  No feasible solution -> branch cut")
            continue

        x = result.x
        cost = result.fun
        print(f"  Relaxed solution: {[round(float(v), 2) for v in x]}  cost = {cost:.2f}")

        # etape C: borne
        # Le cout relache est le meilleur que cette branche puisse donner.
        if cost >= best_cost:
            print(f"  Cost {cost:.2f} >= best {best_cost} -> branch cut")
            continue

        # etape D: Savoir si la solution est faite de nombres entiers?
        i = find_fractional_variable(x)
        if i is None:
            print("  All values are integers -> new best solution!")
            best_cost = cost
            best_x = [round(v) for v in x]
            continue

        # etape E: brancher sur la variable fractionnaire
        # Ex: x11 = 2.5  ->  left: x11 <= 2   right: x11 >= 3
        k = math.floor(x[i])
        low, high = bounds[i]
        print(f"  {NAMES[i]} = {x[i]:.2f} is not an integer -> split into "
              f"{NAMES[i]} <= {k} and {NAMES[i]} >= {k + 1}")

        left = list(bounds)
        left[i] = (low, k)
        right = list(bounds)
        right[i] = (k + 1, high)
        
        nodes_to_explore.append(left)
        nodes_to_explore.append(right)

    return best_x, best_cost

# Execution
if __name__ == "__main__":
    x, cost = branch_and_bound()

    print("\n================ RESULT ================")
    print("        M1  M2  M3")
    print(f"  D1  {x[0]:3d} {x[1]:3d} {x[2]:3d}")
    print(f"  D2  {x[3]:3d} {x[4]:3d} {x[5]:3d}")
    print(f"Minimum total cost = {cost:.0f}")
