import sys
from time import perf_counter

def factors(x):
    return list(sorted([i for i in range(1,x+1) if x%i==0]))

def load_puzzles(file_path):
    with open(file_path) as fileReader:
        line_list = [line.strip() for line in fileReader]

    # calculate N, subblock_width, subblock_height, symbol_set
    data = []
    for puzzle in line_list:
        N = int(len(puzzle) ** 0.5)
        # if int(N ** 0.5) - N ** 0.5 == 0.0: # perfect square
        #     subblock_height, subblock_width = int(N ** 0.5), int(N ** 0.5)
        # the below used to be in the corresponding else block
        # sub-block width is the smallest factor of N greater than its square root
        # for factor in factors(N):
        #     if factor > N ** 0.5:
        #         subblock_width = factor
        #         break
        # print(subblock_width)
        # sub-block height is the greatest factor of N less than its square root
        # for factor in reversed(factors(N)):
        #     if factor < N ** 0.5:
        #         subblock_height = factor
        #         break

        for i in range(int(N ** 0.5), N+1):
            if N % i == 0:
                subblock_width = i
                break
        subblock_height = N//subblock_width

        symbol_set = set([c for c in puzzle if  c not in '.'])
        data.append((N, subblock_width, subblock_height, symbol_set))

    return list(zip(line_list, data))

def print_board(puzzle_state):
    """
    pass  in the full puzzle state which is a tuple
    """
    N = int(puzzle_state[1][0])
    print(N)
    print(f"{N}x{N} PUZZLE")
    for i in range(N):
        for j in range(N):
            print(puzzle_state[0][i*N+j], end=" ")
        print()
    # for i in range(subblock_width):
    #     for j in range(subblock_height):
    #         print(puzzle_state[0][i*subblock_width+j], end=" ")
    #     print()
    # print()

def generate_constraint_sets(puzzle_state):
    """
    generate the sets for row, column, and block conflicts
    should only be run once
    """
    numRows, numCols = int(puzzle_state[1][0]), int(puzzle_state[1][0])
    subblock_height = puzzle_state[1][1]
    subblock_width = puzzle_state[1][2]
    conflicts = {} # {1D Index : [col confls, row confls, block confls]}
    for idx, val in enumerate(puzzle_state[0]):
        cset = set()
        # append all the col conflicts
        for idx2, val in enumerate(puzzle_state[0]):
            if idx2 % int(puzzle_state[1][0]) == idx % int(puzzle_state[1][0]) and idx2 != idx:
                cset.add(idx2)
        # append all row conflicts
        rowIdx = idx // numRows
        rset = set([i+rowIdx*numRows for i in range(numCols)])
        rset.remove(idx)
        # for i in range(numRows):
        #     mat[i] = []
        #     for j in range(numCols):
        #        mat[i].append(puzzle_state[0][i*numCols + j])
        # for a in range(0, len(puzzle_state[0]), numCols):
        #     if (a - )
        colIdx = (idx % numCols)
        blockIdx = (rowIdx//subblock_height, colIdx//subblock_width) # should be the nth block we are at in both dims
        blockcorner = (blockIdx[0] * subblock_height, blockIdx[1] * subblock_width)

        # find all indices of the block

        # find the 1-d index of the block
        blockCornerIndex = blockcorner[0]*numRows + blockcorner[1]

        block_list = [[blockCornerIndex + i for i in range(subblock_width)]]
        for i in range(1, subblock_height):
            newBlockListRow = [a + numRows * i for a in block_list[0]]
            block_list.append(newBlockListRow)
        # flatten block_list and put it into the set
        bset = set([j for sub in block_list for j in sub])
        conflicts[idx] = (cset, rset, bset)
    return conflicts

def symbol_indices(puzzle): # pass in a completed puzzle state
    symbol_set = puzzle[1][3]
    totals = dict.fromkeys(symbol_set, 0)
    for value in puzzle[0]:
        if value != ".":
            totals[value] += 1
    return totals # returns a dictionary: {symbol, # occurences}


def goal_test(puzzle_state):
    return not ("." in puzzle_state[0])

def get_next_unassigned_var(puzzle_state):
    return puzzle_state[0].find(".")

def get_values(state, var, conflicts):
    # get each constraint set
    conflictsets = conflicts[var]
    symbolset_remaining = state[1][3].copy()
    # print(type(symbolset_remaining), "symbolset beginning: ", list(sorted(symbolset_remaining)))
    for s in conflictsets:
        for idx in s:
            if (a:=state[0][idx]) in symbolset_remaining:
                # print("removed ", a, idx, state[0][idx])
                symbolset_remaining.remove(a)
    return symbolset_remaining

def get_sorted_values(state, var, conflicts):
    return get_values(state, var, conflicts)

def sudoku_backtracking(state, conflicts):
    if goal_test(state):
        return state
    var = get_next_unassigned_var(state)
    # print("GOT HERE ONE")
    # print("the values, ", get_sorted_values(state,var,conflicts), state, var)
    for val in get_sorted_values(state, var, conflicts):
        # create new_state by assigning val to var
        new_string = state[0][:var] + val + state[0][var + 1:]
        new_state = (new_string, state[1])
        # print("going to recurse")
        result = sudoku_backtracking(new_state, conflicts)
        if result is not None:
            return result
    return None

if __name__ == "__main__":
    puzzles = load_puzzles(sys.argv[1]) # a puzzle state is (string, (data))
    # print_board(puzzles[0])
    # print(puzzles[0][1])
    for i, puzzle in enumerate(puzzles):
        conflicts = generate_constraint_sets(puzzle)
        # print(conflicts)
        # print(symbol_indices(puzzles[0]))
        newstate = sudoku_backtracking(puzzle, conflicts)
        print(i)
        print(newstate[0])
        print()
        #print_board(newstate)