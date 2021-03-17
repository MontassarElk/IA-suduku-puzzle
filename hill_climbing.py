import math
from sudokuPython3 import *
from SA.SA import *
import random
def init_hill_climbing(values):
    # Dictionary that keeps initial (fixed) values
    fixed_values = dict()
    # Iterate over each section
    for section in UNITLIST[18:]:
        # Get section values as dict
        section_values = {key: value for (key, value) in values.items() if key in section}
        # Create possible values
        possible_values = [value for value in range(1, 10) if str(value) not in section_values.values()]
        # Iterate over section values
        for (key, value) in section_values.items():
            # Case when multiple values are possible
            if  value == '0':
                # Set key as not fixed
                fixed_values[key] = False
                # Assign random possible value
                values[key] = str(possible_values.pop(random.randint(0, len(possible_values) - 1)))
            else:
                # If value is assigned, set as fixed value
                fixed_values[key] = True
    return fixed_values


def evaluate_grid(values):
    score = 0
    # Iterate over rows and columns
    for line in UNITLIST[0:18]:
        # Get line values
        line_values = list(''.join(map(values.__getitem__, line)))
        # Create dictionary that holds {key = assigned_value, value = repetitions)
        line_dict = {i: line_values.count(i) for i in line_values}
        # Iterate over values
        for value in line_dict.values():
            # If number of repetitions is larger than 1, add it to the score
            if value > 1:
                score += value - 1
    return score


def hill_climbing_step(values, fixed_values):



    # Keep our current
    current_score = evaluate_grid(values)
    # Keep track of scores depending on value swap
    swap_scores = dict()
    # Iterate over each section
    for section in UNITLIST[18::]:
        for value in section:
            # IF value is fixed, go to next value
            if fixed_values[value]:
                continue
            # Iterate over other possible values in section
            for other in section:
                # Create unique key assigned to a swap (reduce memory usage for interchangeable swaps)
                key = tuple(sorted([value, other]))
                # If it's the same key, or a fixed value, got to next value
                if other == value or fixed_values[other] or key in swap_scores:
                    continue
                # Make a copy of the grid values
                new_values = values.copy()
                # Swap
                new_values[value], new_values[other] = new_values[other], new_values[value]
                # Assign score to key
                swap_scores[key] = evaluate_grid(new_values)
    # No possible swaps
    if len(swap_scores) == 0:
        return False
    # Check swap with minimal score
    min_key = min(swap_scores, key=swap_scores.get)
    # If score is decreased, then swap the values
    if swap_scores[min_key] < current_score:
        values[min_key[0]], values[min_key[1]] = values[min_key[1]], values[min_key[0]]
        # Return swap keys
        return min_key
    else:
        # No swaps that increase score -- Score might be 0 or algorithm stuck at local minimum
        return False


def hill_climbing(values):
    # Find fixed values and randomly place values in sections

    fixed_values = init_hill_climbing(values)
    while True:
        # Make a step in algorithm

        swap = hill_climbing_step(values, fixed_values)
        # If method returns false, algorithm is done
        # - Either no more swaps are available, or grid is solved

        if not swap:
            return values



def solve_all_hill_climbing(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def time_solve(grid):
        start = time.process_time()
        values = hill_climbing(grid_values(grid))
        t = time.process_time()-start
        # Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values:
                display(values)
            print('(%.2f seconds)\n' % t)
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times)))

solve_all_hill_climbing(from_file("100sudoku.txt"), "sudoku100forannealing", None)