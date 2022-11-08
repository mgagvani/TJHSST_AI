import sys
from time import perf_counter

N, subblock_height, subblock_width, symbol_set, indToBox, boxToInd = 0, 0, 0, set(), dict(), dict()

def print_board(board):
    for row in range(N):
        if row % subblock_height == 0:
            print()
        for split in range(subblock_height):
            left = (N * row + split * subblock_width)
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
    N = int(len(board) ** .5)
    all_symbols = "123456789ABCDEFGHIJKLMNOPQRSTUVQXYZ"
    symbol_set = set(all_symbols[:N])
    if "." in symbol_set:
        symbol_set.remove(".")
    height = -1
    i = int(N ** .5)
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
    l = [i for i in symbol_set if is_valid(state,ind,i)]
    return l

def get_sorted_values(state, ind):
    # we arent sorting or anyting so just return the values
    return get_values(state, ind)

def csp_backtracking(state):
    if "." not in state: # inline the goal test 
        return state
    var = state.index(".") # these really dont have to be functions
    for variable in get_sorted_values(state, var):
        new_state = state[:var] + variable + state[var + 1:]
        result = csp_backtracking(new_state)
        if result is not None:
            return result
    return None

def symbol_instances(state, symbol_set):
    total = 0
    l = list(state)
    for symbol in symbol_set:
        total += l.count(symbol)
    return total

if __name__ == "__main__":
    puzzles = load_puzzles(sys.argv[1]) 
    for _i, puzzle in enumerate(puzzles):
        N, subblock_height, subblock_width, symbol_set, indToBox, boxToInd = make_constraints(puzzle)
        answer = csp_backtracking(puzzle)
        # dont prettyprint
        print(answer)
