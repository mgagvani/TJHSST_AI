# NQUEENS
# Manav Gagvani - 10/18/22

from time import perf_counter
import random

# use globals to prevent having to pass these around all over the place
size = 0
board = []
row_conflicts =  []     
diagr_conflicts = []   
diagl_conflicts = []   

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

def generate_initial_state(size):
    # TODO this can be improved to come up with a decently good starting state
    state = [a for a in range(size)]
    random.shuffle(state)
    return state

def generate_state(size):
    global board
    # put one down every second column
    # 0, 2, 4, etc. 
    l = [None for _a in range(size)]
    used = []
    for i, j in enumerate(range(0, size, 2)):
      l[i] = j
      used.append(j)
    allvals = [n for n in range(size)]
    notused = list(set(allvals) - set(used))
    for ii, vall in enumerate(l):
      if vall is None:
        l[ii] = notused.pop(0)
    # return l
    board = i

def swap(state, x, y):
    temp = state[x]
    state[x] = state[y]
    state[y] = temp # dont return cuz the pointer is still there? NOTE TODO 

def random_swap(state):
    a, b = random.randint(0, len(state)), random.randint(0, len(state))
    swap(state, a, b)

def change_conflicts(col, row, val):
    row_conflicts[row] += val
    diagr_conflicts[col + row] += val
    diagl_conflicts[col + (size - row - 1)] += val
    totalConflicts = sum(diagl_conflicts) + sum(diagr_conflicts) + sum(row_conflicts)

def min_conflict_pos(col):
    minConflicts = size
    minConflictRows = []
    for row in range(size):
        conflicts = row_conflicts[row] + diagr_conflicts[col + row] + diagl_conflicts[col + (size - row - 1)]
        if conflicts == 0:
            return row
        if conflicts < minConflicts:
            minConflictRows = [row]
            minConflicts = conflicts
        elif conflicts == minConflicts:
            minConflictRows.append(row)
    # randomly choose the index from the list of tied conflict values
    choice = random.choice(minConflictRows)
    return choice

# setup board so that it minimizes the conflicts initially
def create_minimized_board():
    global board
    global row_conflicts
    global diagr_conflicts
    global diagl_conflicts
    global size

    board = []

    # Initialize conflict arrs
    diagr_conflicts = [0] * ((2 * size) - 1)
    diagl_conflicts = [0] * ((2 * size) - 1)
    row_conflicts = [0] * size

    rowSet = set(range(0,size))
    notPlaced = []

    for col in range(0, size):
        testRow = rowSet.pop()
        conflicts = row_conflicts[testRow] + diagr_conflicts[col + testRow] + diagl_conflicts[col + (size- testRow - 1)]
        if conflicts == 0:
            board.append(testRow)
            change_conflicts(col, board[col], 1)
        else:
            rowSet.add(testRow)
            testRow2 = rowSet.pop()
            conflicts2 = row_conflicts[testRow2] + diagr_conflicts[col + testRow2] + diagl_conflicts[col + (size- testRow2 - 1)]
            if not conflicts2:
                board.append(testRow2)
                change_conflicts(col, board[col], 1)
            else:
                rowSet.add(testRow2)
                board.append(None)
                notPlaced.append(col)

    for col in notPlaced:
        board[col] = rowSet.pop()
        change_conflicts(col, board[col], 1)

    totalConflicts = sum(diagl_conflicts) + sum(diagr_conflicts) + sum(row_conflicts)
    print(f"Conflicts: {totalConflicts} conflicts")


def max_conflict_col():
    conflicts, maxConflicts, maxConflictCols = 0, 0, []

    for col in range(size):
            row = board[col]
            conflicts = row_conflicts[row] + diagr_conflicts[col+row] + diagl_conflicts[col+(size-row-1)]
            if (conflicts > maxConflicts):
                    maxConflictCols = [col]
                    maxConflicts = conflicts
            elif conflicts == maxConflicts:
                    maxConflictCols.append(col)
    choice = random.choice(maxConflictCols)
    return choice, maxConflicts


def nqueens_iterative3():
    create_minimized_board()
    print("FINISHED MINIMIZED BOARD")
    iteration, maxIteration = 0, size

    while (iteration < maxIteration): # so that it doesnt go forever
        col, numConflicts = max_conflict_col()
        print(numConflicts)
        if (numConflicts > 3): # cannot swap if there are only 2 bc infinte loop
            newLocation = min_conflict_pos(col)
            if (newLocation != board[col]):
                change_conflicts(col, board[col], -1)
                board[col] = newLocation
                change_conflicts(col, newLocation, 1)
        iteration += 1
    return board

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
    sizes = (8,)# (19, 23, 29, 43, 49, 97)
    # sizes = [a for a in range(15, 30, 4)]
    # sizes.append(31)
    # sizes.append(51)
    for i in sizes:
        state = [None for _b in range(i)]

        safeidx = [[a for a in range(i)] for b in range(i)]

        a =  perf_counter()
        # METHOD GOES HERE
        # solution = nqueens_backtracking(state)
        # solution = nqueens_iterative(i, i**5)
        size = i
        solution = nqueens_iterative3()
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