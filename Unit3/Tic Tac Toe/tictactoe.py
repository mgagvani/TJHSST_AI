import sys
from time import perf_counter
from collections import deque

BOARD = "........."

def game_over0(board):
    axes = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    return any("".join(board[p] for p in axis) in ["XXX","OOO"] for axis in axes)

def game_over(board):
    """
    returns a boolean saying if the game is over or not
    """
    a = board
    # row
    if a[0] == a[1] and a[1] == a[2] and a[0] == a[2]:
        return True
    elif a[3] == a[4] and a[4] == a[5] and a[3] == a[5]:
        return True
    elif a[6] == a[7] and a[7] == a[8] and a[6] == a[8]:
        return True
    # column
    elif a[0] == a[3] and a[3] == a[6] and a[0] == a[6]:
        return True
    elif a[1] == a[4] and a[4] == a[7] and a[1] == a[7]:
        return True
    elif a[2] == a[5] and a[5] == a[8] and a[2] == a[8]:
        return True
    # diag
    elif a[0] == a[4] and a[4] == a[8] and a[0] == a[8]:
        return True
    elif a[2] == a[4] and a[4] == a[6] and a[2] == a[6]:
        return True
    
    else:
        return False

def game_over2(board):
    """
    returns information on who won, or possible draws
    """
    a = board
    # row
    if a[0] == a[1] and a[1] == a[2] and a[0] == a[2]  and a[0]:
        return a[0]
    elif a[3] == a[4] and a[4] == a[5] and a[3] == a[5]:
        return a[3]
    elif a[6] == a[7] and a[7] == a[8] and a[6] == a[8]:
        return a[6]
    # column
    elif a[0] == a[3] and a[3] == a[6] and a[0] == a[6]:
        return a[0]
    elif a[1] == a[4] and a[4] == a[7] and a[1] == a[7]:
        return a[1]
    elif a[2] == a[5] and a[5] == a[8] and a[2] == a[8]:
        return a[2]
    # diag
    elif a[0] == a[4] and a[4] == a[8] and a[0] == a[8]:
        return a[0]
    elif a[2] == a[4] and a[4] == a[6] and a[2] == a[6]:
        return a[2]
    elif not "." in a:
        return "~DRAW"
    
    else:
        return False

def game_over3(c, n):
    """
    c is the state and n is the one we are checking for
    """
    if c[0] == n and c[1] == n and c[2] == n   != ".": return 1
    elif c[3] == n and c[4] == n and c[5] == n != ".": return 1
    elif c[6] == n and c[7] == n and c[8] == n != ".": return 1  
    elif c[0] == n and c[3] == n and c[6] == n != ".": return 1
    elif c[1] == n and c[4] == n and c[7] == n != ".": return 1
    elif c[2] == n and c[5] == n and c[8] == n != ".": return 1  
    elif c[0] == n and c[4] == n and c[8] == n != ".": return 1
    elif c[2] == n and c[4] == n and c[6] == n != ".": return 1 
    elif not "." in c: return 1
    return 0

def game_over2a(board):
    x = game_over2(board)
    if x == ".":
        return False
    else:
        return x

def game_over3a(board):
    return (game_over3(board, "X") or game_over3(board, "O"))

def to_mat2(s, n):
    """
    copied from slider puzzles
    """
    return list(map(list, zip(*[map(str, s)] * n)))

def print_board(board):
    for row in to_mat2(board, 3):
        print(" ".join(row))

def all_possible_moves(board):
    dot_indices = [i for i, ltr in enumerate(board) if ltr == '.']
    moves = set()
    for index in dot_indices:
        _listO = list(board)
        _listX = list(board)
        _listO[index] = "O"
        _listX[index] = "X"
        moves.add("".join(_listX))
        moves.add("".join(_listO))
    return moves

def all_possible_moves(board, current):
    dot_indices = [i for i, ltr in enumerate(board) if ltr == '.']
    moves = set()
    for index in dot_indices:
        _list = list(board)
        _list[index] = current
        moves.add("".join(_list))
    return moves

def generate_all_states(start):
    fringe = deque()
    visited = set()
    fringe.append((start, 0))
    visited.add(start)
    current = "X"
    layers = {}
    while len(fringe) > 0:
        if current == "X":
            current = "O"
        elif current == "O":
            current = "X"
        else:
            print("bro come on")
        v, _l = fringe.popleft() # DIS IS PARENT
        if (x:=game_over2a(v)):
            string = x + str(_l)
            if not string in layers.keys():
                layers[string] = 0
            else:
                layers[string] += 1
            # print_board(v)
            # print(v, _l, layers[string], string)
            # input()
        for child in all_possible_moves(v, current):
            if child not in visited:
                fringe.append((child, _l + 1)) # ADD ONE TO PARENT"S LEVEL
                visited.add(child)
    for k in sorted(layers.keys()):
        print(k, layers[k])
    print(sum(layers.values()))
    return len(visited)

"""
PSEUDO CODE
x_move:
    if game is over:
        add to final states set
        stop
    for each period in the board:
        play x there
        o_move(new board)
"""

states = []
moves = 0
def o_move(board):
    global moves
    if game_over3a(board):
        mcount = 9-list(board).count(".")
        states.append((board, str(game_over2a(board))+str(mcount)))
        return
    amoves = all_possible_moves(board, "O")
    moves += 1
    for nboard in amoves:
        x_move(nboard)

def x_move(board):
    global moves
    if game_over3a(board):
        mcount = 9-list(board).count(".")
        states.append((board, str(game_over2a(board))+str(mcount)))
        return
    amoves = all_possible_moves(board, "X")
    moves += 1
    for nboard in amoves:
        o_move(nboard)

def generate_stats(board):
    x_move(board)
    print(len(states))
    print(len(set(states)))
    results = {}
    for state in states:
        board, key = state[0], state[1]
        if key not in results.keys():
            results[key] = 1
        else:
            results[key] += 1
    for key in results.keys():
        print(key, results[key])
    print(sum(results.values()))

# 255168
# 958
# X5 - 120
# X7 - 444
# X9 - 62
# O6 - 148
# O8 - 168
# DRAW - 16

# 1 means X won, 0 means draw, -1 means O won

def generate_score(board):
    if (x:=game_over2a(board)) == 'X':
        return 1
    elif x == 'O':
        return -1
    else:
        return 0

def get_player(c):
    if c == 'X':
        return 'O'
    elif c == 'O':
        return "X"
    else:
        raise NameError("bro come on its not even the right name")

def min_step(board, c):
    if game_over3a(board):
        return (generate_score(board), board)
    results = []
    for next_board in all_possible_moves(board, c):
        results.append((max_step(next_board, get_player(c))[0], next_board))
    return sorted(results)[0]

def max_step(board, c):
    if game_over3a(board):
        return (generate_score(board), board)
    results = []
    for next_board in all_possible_moves(board, c):
        results.append((min_step(next_board, get_player(c))[0], next_board))
    return sorted(results, reverse=True)[0]

def human_move(board, curr):
    print_board(board)
    available = [i for i, ltr in enumerate(board) if ltr == '.']
    print(f"Available indices: {available}")
    index = input(f"Which index do you want to place a {curr} on? (0-8) ")
    while index not in available:
        index = input(f"Come on give me something valid: ")
    lboard = list(board)
    lboard[index] = curr
    return "".join(lboard)

def ai_move(board, curr):
    if curr == 'X':
        expected, board = max_step(board, curr)
    elif curr == 'O':
        expected, board = max_step(board, curr)
    else:
        raise ValueError("Bro what is this")
    human_move(board, get_player(board))



if __name__ == "__main__":
    # board = "........."
    board = "XX..OOO.."
    print_board(board)
    curr = 'O'
    print()
    print_board(max_step(board, curr)[1])

    
    


