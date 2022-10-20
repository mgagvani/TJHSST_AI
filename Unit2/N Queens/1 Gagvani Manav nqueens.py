# NQUEENS
# Manav Gagvani - 10/18/22

from time import perf_counter

# Global SAFEIDX

def goal_test(state):
    return (not (None in state))

def get_next_unassigned_var(state):
    return state.index(None)

def generate_safeidx(state, var, size, safeidx):
    if var == 0: # dont even bother doing anything
        return safeidx
    # reset anything below me if I have backtracked (the row is too high for to have "been there")
    # for z, row in enumerate(safeidx[var:]):
    #     safeidx[var + z] = [aa for aa in range(size)]
    for z, row in enumerate(safeidx):
        safeidx[z] = [aa for aa in range(size)]
    # otherwise, determine vertical/diagonal un-safeties
    for queenrow, queencol in enumerate(state[:var]):
        # remove vertical conflicts
        for i, row in enumerate(safeidx):
            try:
                safeidx[i].remove(queencol)
            except ValueError:
                pass
        # remove diagonal conflicts (we only need to go down)
        for a in range(size):
            colnum = queencol + a # right
            colnum2 = queencol - a # left 
            rownum = queenrow + a
            if (colnum > 0) and (colnum < size) and (rownum > 0) and (rownum < size):
                try:
                    safeidx[rownum].remove(colnum)
                except ValueError:
                    pass
            if (colnum2 > 0) and (colnum2 < size) and (rownum > 0) and (rownum < size):
                try:
                    safeidx[rownum].remove(colnum2)
                except ValueError:
                    pass
    return safeidx
        
def get_sorted_values2(state, var, safeidx):
    size = len(state)
    safeidx = generate_safeidx(state, var, size, safeidx)
    # generate new state
    # print(var, safeidx[var], state)
    return safeidx[var]

def nqueens_backtracking2(state, safeidx):
    if goal_test(state): return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values2(state, var, safeidx):
        # create new_state by assigning val to var
        new_state = state.copy(); new_state[var] = val
        result = nqueens_backtracking2(new_state, safeidx)
        if result is not None:
            return result
    return None

def get_values(state, var): # var is current row
    _abs = abs
    size = len(state)
    possible_values = [a for a in range(size)]
    # iterate over every queen already there
    for queenrow, queen_idx in enumerate(state[:var]):
        # remove candidates directly in front
        if queen_idx in possible_values:
            possible_values.remove(queen_idx)
        # remove candidates diagonally 
        for candidate in possible_values.copy(): # prevent concurrent modification
            if _abs(queenrow - var) == _abs(queen_idx - candidate): # the vertical delta (left) equals horizontal delta (right)
                possible_values.remove(candidate)
    return possible_values

def get_sorted_values(state, var):
    _abs = abs
    size = len(state)
    a = get_values(state,var)
    sort_by_list = [_abs(size//2 - value) for value in a]
    return [x for _, x in sorted(zip(sort_by_list, a))]

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
    start = perf_counter()
    # sizes = (8,17,18,29,30,31,32)
    sizes = [a for a in range(15, 30, 4)]
    sizes.append(31)
    sizes.append(35)
    for i in sizes:
        state = [None for _b in range(i)]

        safeidx = [[a for a in range(i)] for b in range(i)]

        a =  perf_counter()
        solution = nqueens_backtracking(state)
        b = perf_counter()

        # aa = perf_counter()
        # solution = nqueens_backtracking2(state, safeidx)
        # bb = perf_counter()

        print(i, solution, test_solution(solution), b-a, "seconds")
        # print(i, solution, test_solution(solution), bb-aa, "seconds, old algo:",b-a)
    end = perf_counter()
    print(f"TOTAL TIME: {end - start} seconds")

'''
COPY 2D ARRAY
n_ls = [x.copy() for x in ls]

CCOPY DICT OF LISTS
e = {x : d[x].copy() for x in d}
'''