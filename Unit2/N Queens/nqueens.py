# NQUEENS
# Manav Gagvani - 10/18/22

from time import perf_counter

def goal_test(state):
    return (not (None in state))

def get_next_unassigned_var(state):
    return state.index(None)

def get_sorted_values(state, var): # var is current row
    size = len(state)
    possible_values = [a for a in range(size)]
    # iterate over every queen already there
    for queenrow, queen_idx in enumerate(state[:var]):
        # remove candidates directly in front
        if queen_idx in possible_values:
            possible_values.remove(queen_idx)
        # remove candidates diagonally 
        for candidate in possible_values.copy(): # prevent concurrent modification
            if abs(queenrow - var) == abs(queen_idx - candidate): # the vertical delta (left) equals horizontal delta (right)
                possible_values.remove(candidate)
    return possible_values

def nqueens_backtracking(state):
    if goal_test(state): return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        # create new_state by assigning val to var
        new_state = state.copy(); new_state[var] = val
        result = nqueens_backtracking(new_state)
        if result is not None:
            return result
    return None

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                return False
    return True

if __name__ == "__main__":
    for i in range(8, 25):
        state = [None for _b in range(i)]

        a =  perf_counter()
        solution = nqueens_backtracking(state)
        b = perf_counter()

        print(solution, test_solution(solution), b-a, "seconds")

'''
COPY 2D ARRAY
n_ls = [x.copy() for x in ls]

CCOPY DICT OF LISTS
e = {x : d[x].copy() for x in d}
'''