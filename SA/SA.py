from sudoku import *
import math
import random

### Les variables globales

squareList = ['A1', 'A4', 'A7', 'D1', 'D4', 'D7', 'G1', 'G4', 'G7']
tab = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
lines = [[j + str(i) for i in range(1, 10)] for j in tab]
cols = [[j + str(i) for j in tab] for i in range(1, 10)]
squares_3x3 = unitlist[18:]




## Notre fonction Display qui affiche le grille 2-D clairement
def my_display(values):
    sortedKeys = sorted(values)
    for i in range(0, 9):
        if i != 0 and i % 3 == 0:
            print("- - - + - - - + - - -")
        for j in range(0, 9):
            if j != 0 and j % 3 == 0:
                print("|", end=' ')
            key = sortedKeys[i * 9 + j]
            print(values[key], end=' ')
        print()

"""
Fonction qui extraire les differente
valeurs sur les colonnes du sudoku
"""
def get_cols_val(values):
    val_col = []
    ## parcours les colones
    for col in cols:
        tab = []
        for c in col:
            tab.append(values[c])
        val_col.append(tab)
    return val_col


"""

Fonction qui extraire les differente
valeurs sur les lignes du sudoku

"""
def get_lines_val(values):
    val_col = []
    for line in lines:
        tab = []
        for c in line:
            tab.append(values[c])
        val_col.append(tab)
    return val_col


'''
 fonction qui determine les 
 positions deja fixe au debut du
 programme.
'''
def get_fixied(value):

    fixed = []

    for item in squareList:

        square = units[item][2]
        tab = []
        for pos in square:
            if value[pos] in '.0':
                tab.append(pos)
        fixed.append(tab)
    return fixed
"""
    Choisir deux positions au hasard dans un carre au hasard et les interchange.
"""
def flip_random_pair(values, fixed):
    square = random.choice(squares_3x3)
    positions = [i for i in square if i not in fixed]
    if (len(positions) < 2): return flip_random_pair(values, fixed)

    pos1, pos2 = random.sample(positions, k=2)

    temp = values[pos1]
    values[pos1] = values[pos2]
    values[pos2] = temp
    return pos1,pos2



'''
 Remplie de facon ramdon les positions 
 vide d'un carree
'''
def fill_random_square(value,square):

    for pos in square:
        if value[pos] in '.0':
            square_val = [value[i] for i in square]
            number = [int(x) for x in square_val if x not in '.0']
            choice_rand = [x for x in range(1,10) if x not in number]
            nb = random.choice( choice_rand)
            value[pos] = str(nb)
    return value
'''
Remplie de facon aleatoire les positions
vides de chaque carree du sudoku
'''
def fill_squares_by_random(value):

    for item in squareList:

        square = units[item][2]
        value = fill_random_square(value,square)
    return value

'''calcule le nombre de nombre repetition de chaque
differents nombre dans les colonnes du sudoku'''
def count_row_error(values):
    conflicts = 0


    for col in cols:

        numbers = set([values[i] for i in col])

        conflicts += (9 - len(numbers))
    return conflicts
"""
    Compte le nombre d'erreur de chaque ligne c'est-a-dire
    le nombre de repetion differente dun nomnbre
"""
def count_lines_error(values):
    conflicts = 0
    for line in lines:
        numbers = set([values[i] for i in line])
        conflicts += (9 - len(numbers))
    return conflicts

'''
Faire le swap entre deux positons
'''
def swap(pos1, pos2, val):
    values = val.copy()
    temp = values[pos1]

    values[pos1] = values[pos2]
    values[pos2] = temp

    return values


"""
La fonction simaled annealing

"""
def SA(value):
    fixed = get_fixied(value)
    ## remplir par random au debut
    value = fill_squares_by_random(value)



    ## calculer le score courrant
    current_score = count_row_error(value) + count_lines_error(value)
    temperature = 3
    alpha = 0.99
    if current_score == 0:
        return value

    while current_score != 0:

        # my_display(value)
        pos1,pos2 = flip_random_pair(value.copy(),fixed)

        val = swap(pos1,pos2,value)

        new_socre = count_row_error(val) + count_lines_error(val)

        # doit-on faire le swap??
        should_swap = False

        if new_socre < current_score:
            should_swap = True

        else:
            diff = new_socre - current_score
            eq = math.exp(-diff / temperature)
            if random.random() < eq:
                should_swap = True

        if should_swap or (current_score == new_socre):
            current_score = new_socre
            value = val.copy()
        else:
            pass
        temperature *= alpha

    return value




def solve_simulated_annealing(grid):
    values = grid_values(grid)

    values = SA(values)

    return values


def solve_all_simulated_annealing(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""

    def time_solve(grid):
        start = time.perf_counter()
        values = solve_simulated_annealing(grid)
        t = time.perf_counter() - start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print('(%.3f seconds)\n' % t)

        return (t, solved(values))

    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.3f secs (%d Hz), max %.3f secs)." % (
            sum(results), N, name, sum(times) / N, N / sum(times), max(times)))



if __name__ == '__main__':

    solve_all_simulated_annealing(from_file("1000sudoku.txt"), "sudoku100forannealing", None)
