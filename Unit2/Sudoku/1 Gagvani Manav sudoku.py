# Manav Gagvani - 11/8/22
# To format: "black 1 Gagvani Manav sudoku.py"
# To run with profiler: "python -m cProfile -s tottime "1 Gagvani Manav sudoku.py" puzzles_1_standard_easy.txt"

import sys
from time import perf_counter


N, subblock_height, subblock_width, symbol_set, indToBox, boxToInd = (
    0,
    0,
    0,
    set(),
    dict(),
    dict(),
)


def print_board(board):
    for row in range(N):
        if row % subblock_height == 0:
            print()
        for split in range(subblock_height):
            left = N * row + split * subblock_width
            right = N * row + (split + 1) * subblock_width
            print(" ".join(board[left:right]), end="   ")
        print()


def load_puzzles(file_path):
    with open(file_path) as fileReader:
        line_list = [line.strip() for line in fileReader]
    return line_list


def make_constraints(board):
    """
    init the board and it's constraints
    """
    N = int(len(board) ** 0.5)
    all_symbols = "123456789ABCDEFGHIJKLMNOPQRSTUVQXYZ"
    symbol_set = set(all_symbols[:N])
    if "." in symbol_set:
        symbol_set.remove(".")
    height = -1
    i = int(N**0.5)
    while i < N and height == -1:
        if N % i == 0:
            height = i
        i += 1
    width = N // height

    indToBox = {}  # {0:0,1:0,2:1}
    boxToInd = {}  # {0:[0,1],1:[2,3]}
    box = -1
    for x in range(height * width):
        if x % height != 0:
            box -= height
        for y in range(height * width):
            ind = x * height * width + y
            if y % width == 0:
                box += 1
            indToBox[ind] = box
            lis = boxToInd.get(box, [])
            boxToInd[box] = lis + [ind]
    return N, height, width, symbol_set, indToBox, boxToInd


def forward_look(mdict, index, symbol, ones):
    _len = len
    mdict[index] = ""
    box = indToBox[index]
    for ind in boxToInd[box]:
        # if ind!=index and state[ind]==".":
        a = mdict[ind]
        if symbol in a:
            a = a.replace(symbol, "")
            if _len(a) == 1:
                ones.add(ind)
            if _len(a) == 0:
                return None, None
            mdict[ind] = a
    row = index // N
    for ind in range(N * row, N * (row + 1)):
        a = mdict[ind]
        if symbol in a:
            a = a.replace(symbol, "")
            if _len(a) == 1:
                ones.add(ind)
            if _len(a) == 0:
                return None, None
            mdict[ind] = a
    col = index % N
    for ind in range(col, N * (N) + col, N):
        a = mdict[ind]
        if symbol in a:
            a = a.replace(symbol, "")
            if _len(a) == 1:
                ones.add(ind)
            if _len(a) == 0:
                return None, None
            mdict[ind] = a
    return mdict, ones


def is_valid(state, ind, symbol):
    """
    check if a symbol can be placed in the index
    """
    row = ind // N
    col = ind % N
    box = indToBox[ind]
    for r in range(N):  # checks every character in column
        indy = r * N + col
        if state[indy] == symbol:
            return False
        # for r in range(N): #checks every character in row
        indl = row * N + r
        if state[indl] == symbol:
            return False
    for index in boxToInd[box]:
        if state[index] == symbol:
            return False
    return True


def get_values(state, ind):
    """
    tries each symbol and if it works out then add it to the list
    """
    l = [i for i in symbol_set if is_valid(state, ind, i)]
    return l


def get_sorted_values(state, ind):
    # we arent sorting or anyting so just return the values
    return get_values(state, ind)


def get_sorted_values2(dictionary, ind):
    return dictionary[ind]


def get_next_unassigned_variable(possible, ones):
    """
    now it chooses the index with the minimum possible choices - most constrained
    """
    _len = len
    if _len(ones) > 0:
        return ones.pop() # this removes a random one
    minNum = 100
    minInd = -1
    for index in range(N**2):
        if 0 < _len(possible[index]) < minNum:
            minNum = len(possible[index])
            minInd = index
    return minInd


def csp_backtracking(state):
    if "." not in state:  # inline the goal test
        return state
    var = state.index(".")  # these really dont have to be functions
    for variable in get_sorted_values(state, var):
        new_state = state[:var] + variable + state[var + 1 :]
        result = csp_backtracking(new_state)
        if result is not None:
            return result
    return None


def populate(puzzle):
    _len = len
    options = []
    ones = set()
    for index in range(len(puzzle)):
        ad = ""
        if puzzle[index] == ".":
            ad = "".join(
                [symbol for symbol in symbol_set if is_valid(puzzle, index, symbol)]
            )
            if _len(ad) == 1:
                ones.add(index)
        options.append(ad)
    return options, ones


def constraint_propagation(state, dict):
    state_list = list(state)
    for box in range(N):
        objects = [state_list[index] for index in boxToInd[box]]
        for symbol in symbol_set:
            if symbol not in objects:
                present = [symbol in dict[index] for index in boxToInd[box]]
                c = present.count(True)
                if c == 0:
                    return None, None
                elif c == 1:
                    idx = boxToInd[box][present.index(True)]
                    # state = state[:idx] + symbol + state[idx + 1 :]
                    state_list[idx] = symbol
                    dict[idx] = ""
    for row in range(N):
        objects = [state_list[index] for index in range(N * row, N * (row + 1))]
        for symbol in symbol_set:
            if symbol not in objects:
                present = [
                    symbol in dict[index] for index in range(N * row, N * row + N)
                ]
                c = present.count(True)
                if c == 0:
                    return None, None
                elif c == 1:
                    idx = row * N + present.index(True)
                    # state = state[:idx] + symbol + state[idx + 1 :]
                    state_list[idx] = symbol
                    dict[idx] = ""
    for col in range(N):
        for row in range(N):
            objects = [state_list[index] for index in range(col, N**2 + col, N)]
            for symbol in symbol_set:
                if symbol not in objects:
                    present = [
                        symbol in dict[index] for index in range(col, N**2 + col, N)
                    ]
                    c = present.count(True)
                    if c == 0:
                        return None, None
                    elif c == 1:
                        idx = col + N * present.index(True)
                        # state = state[:idx] + symbol + state[idx + 1 :]
                        state_list[idx] = symbol
                        dict[idx] = ""
    newstate = "".join(state_list)
    # TODO add forward looking right here
    # assert (state == newstate)
    return newstate, dict


def csp_backtracking2(state, dict_constraint, ones):
    """
    backtracking with forward looking and constraint propagation
    """
    # print(ones)
    if "." not in state:
        return state
    # do forward looking
    # print(ones, state)
    # input()
    if len(ones) == 0:
        state, dict_constraint = constraint_propagation(state, dict_constraint)
        if dict_constraint is None:
            return None
        if "." not in state:
            return state

    idx = get_next_unassigned_variable(dict_constraint, ones)
    for symbol in get_sorted_values2(dict_constraint, idx):
        new_state = state[:idx] + symbol + state[idx + 1 :]
        new_dict = dict_constraint.copy()
        new_dict[idx] = ""
        new_dict, new_ones = forward_look(new_dict, idx, symbol, ones.copy())
        if new_dict is not None:
            result = csp_backtracking2(new_state, new_dict, new_ones)
            if result is not None:
                return result
    return None


def symbol_instances(state, symbol_set):
    """
    counts the number of valid symbols in the puzzle state. this generally should be increasing
    """
    total = 0
    l = list(state)
    for symbol in symbol_set:
        total += l.count(symbol)
    return total


if __name__ == "__main__":
    puzzles = load_puzzles(sys.argv[1])
    for _i, puzzle in enumerate(puzzles):
        (
            N,
            subblock_height,
            subblock_width,
            symbol_set,
            indToBox,
            boxToInd,
        ) = make_constraints(puzzle)
        dict, ones = populate(puzzle)
        result = csp_backtracking2(puzzle, dict, ones)
        print(result)
