import sys
from time import perf_counter
from collections import deque

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
def o_move(board):
    if game_over3a(board):
        states.append(board)
        return
    moves = all_possible_moves(board, "O")
    for nboard in moves:
        x_move(nboard)

def x_move(board):
    if game_over3a(board):
        states.append(board)
        return
    moves = all_possible_moves(board, "X")
    for nboard in moves:
        o_move(nboard)

# 255168
# 958

if __name__ == "__main__":
    board = "........."
    print_board(board)
    x_move(board)
    print(len(states))
    print(len(set(states)))
