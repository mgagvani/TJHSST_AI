import sys
from collections import deque

BOARD = "........."
Oo = "OOO"
Xx = "XXX"


def game_over0(board):
    axes = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    return any("".join(board[p] for p in axis) in ["XXX", "OOO"] for axis in axes)


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
    if a[0] == a[1] and a[1] == a[2] and a[0] == a[2] and a[0]:
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
    if c[0] == n and c[1] == n and c[2] == n != ".":
        return 1
    elif c[3] == n and c[4] == n and c[5] == n != ".":
        return 1
    elif c[6] == n and c[7] == n and c[8] == n != ".":
        return 1
    elif c[0] == n and c[3] == n and c[6] == n != ".":
        return 1
    elif c[1] == n and c[4] == n and c[7] == n != ".":
        return 1
    elif c[2] == n and c[5] == n and c[8] == n != ".":
        return 1
    elif c[0] == n and c[4] == n and c[8] == n != ".":
        return 1
    elif c[2] == n and c[4] == n and c[6] == n != ".":
        return 1
    elif not "." in c:
        return "DRAW"
    return 0


def game_over2a(board):
    x = game_over2(board)
    if x == ".":
        return False
    else:
        return x


def game_over3a(board):
    return game_over3(board, "X") or game_over3(board, "O")


def game_over4(board):
    if board[0:3] == Xx or board[3:6] == Xx or board[6:9] == Xx:
        return (True, 1)
    if board[0:7:3] == Xx or board[1:8:3] == Xx or board[2:9:3] == Xx:
        return (True, 1)
    if board[0:9:4] == Xx or board[2:7:2] == Xx:
        return (True, 1)
    if board[0:3] == Oo or board[3:6] == Oo or board[6:9] == Oo:
        return (True, -1)
    if board[0:7:3] == Oo or board[1:8:3] == Oo or board[2:9:3] == Oo:
        return (True, -1)
    if board[0:9:4] == Oo or board[2:7:2] == Oo:
        return (True, -1)
    if board.find(".") == -1:
        return (True, 0)
    return (False, 0)


def to_mat2(s, n):
    """
    copied from slider puzzles
    """
    return list(map(list, zip(*[map(str, s)] * n)))


def print_board(board):
    for row in to_mat2(board, 3):
        print(" ".join(row))


def all_possible_moves0(board):
    dot_indices = [i for i, ltr in enumerate(board) if ltr == "."]
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
    dot_indices = [i for i, ltr in enumerate(board) if ltr == "."]
    moves = set()
    for index in dot_indices:
        _list = list(board)
        _list[index] = current
        moves.add("".join(_list))
    return moves


def all_possible_moves2(board, current):
    dot_indices = [i for i, ltr in enumerate(board) if ltr == "."]
    moves = set()
    for index in dot_indices:
        _list = list(board)
        _list[index] = current
        moves.add(("".join(_list), index))
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
        v, _l = fringe.popleft()  # DIS IS PARENT
        if x := game_over2a(v):
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
                fringe.append((child, _l + 1))  # ADD ONE TO PARENT"S LEVEL
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
        mcount = 9 - list(board).count(".")
        states.append((board, str(game_over2a(board)) + str(mcount)))
        return
    amoves = all_possible_moves(board, "O")
    moves += 1
    for nboard in amoves:
        x_move(nboard)


def x_move(board):
    global moves
    if game_over3a(board):
        mcount = 9 - list(board).count(".")
        states.append((board, str(game_over2a(board)) + str(mcount)))
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
    if (x := game_over2a(board)) == "X":
        return 1
    elif x == "O":
        return -1
    else:
        return 0


def get_player(c):
    if c == "X":
        return "O"
    elif c == "O":
        return "X"
    else:
        raise NameError("bro come on its not even the right name")


def explain_ai(dict):
    for idx, val in dict.items():
        a, c = val
        if a == 1 and c == "X":
            winner = True
            draw = False
        elif a == -1 and c == "O":
            winner = True
            draw = False
        elif a == 1 and c == "O":
            winner = False
            draw = False
        elif a == -1 and c == "X":
            winner = draw = False
        elif a == 0:
            winner = False
            draw = True
        else:
            raise NotImplementedError(
                "something bad happened and this message should get your attention"
            )
        if draw:
            ret = "draw"
        elif winner:
            ret = "win"
        else:
            ret = "loss"
        print(f"Moving at {idx} results in a {ret}.")


def min_step0(board, c):
    if game_over3a(board):
        return (generate_score(board), board)
    results = []
    info = {}
    for next_board, idx in all_possible_moves2(board, c):
        a = max_step(next_board, get_player(c))[0]
        info[idx] = (a, c)
        results.append((a, next_board))
    # explain_ai(info)
    return sorted(results)[0]


def max_step0(board, c):
    if game_over3a(board):
        return (generate_score(board), board)
    results = []
    info = {}
    for next_board, idx in all_possible_moves2(board, c):
        a = min_step(next_board, get_player(c))[0]
        info[idx] = (a, c)
        results.append((a, next_board))
    # explain_ai(info)
    return sorted(results, reverse=True)[0]


def strify(board):
    """
    converts board to string
    """
    if type(board) is tuple:
        return board[0]
    if type(board) in (int, float, dict, bool):
        print("the board isn't valid")
    if type(board) != str:
        return "".join(board)
    else:
        return board


def max_step(board):
    board = strify(board)
    game_condition, score = game_over4(board)
    if game_condition == True:
        return score
    results = []
    for next_board in all_possible_moves2(board, "X"):
        results.append(min_step(next_board))
    return max(results)


def min_step(board):
    board = strify(board)
    game_condition, score = game_over4(board)
    if game_condition == True:
        return score
    results = []
    for next_board in all_possible_moves2(board, "O"):
        results.append(max_step(next_board))

    return min(results)


def human_move(board, curr):
    print_board(board)
    available = [i for i, ltr in enumerate(board) if ltr == "."]
    if len(available) == 0 or game_over3a(board):
        return board
    print(f"Available indices: {available}")
    index = int(input(f"Which index do you want to place a {curr} on? (0-8) "))
    while index not in available:
        index = int(input(f"Come on give me something valid: "))
    lboard = list(board)
    lboard[index] = curr
    print()
    return "".join(lboard)


def explain_ai2(board, func, curr):
    outcomes = []
    idxs = []
    # print(func)
    for next_board, idx in all_possible_moves2(board, curr):
        print(game_over3(next_board, curr), idx)
        print(game_over3(next_board, get_player(curr)), idx)
        print()
        if game_over3(board, curr) == 1:
            outcomes.append(1)
            idxs.append(idx)
            continue
        elif game_over3(board, get_player(curr)) == 1:
            outcomes.append(-1)
            idxs.append(idx)
            continue
        elif game_over3(board, curr) == "DRAW":
            outcomes.append(0)
            idxs.append(idx)
            continue
        else:  # keep on going
            outcomes.append(func(next_board, curr)[0])
            idxs.append(idx)
    # print(outcomes)
    # print(idxs)
    c = curr
    for i, a in enumerate(outcomes):
        if a == 1 and c == "X":
            winner = True
            draw = False
        elif a == -1 and c == "O":
            winner = True
            draw = False
        elif a == 1 and c == "O":
            winner = False
            draw = False
        elif a == -1 and c == "X":
            winner = draw = False
        elif a == 0:
            winner = False
            draw = True
        else:
            raise NotImplementedError(
                "something bad happened and this message should get your attention"
            )
        if draw:
            ret = "draw"
        elif winner:
            ret = "win"
        else:
            ret = "loss"
        print(f"Moving at {idxs[i]} results in a {ret}.")


def ai_move(board, curr):
    if curr == "X":
        explain_ai2(board, min_step, curr)
        _expected, board = max_step(board, curr)
    elif curr == "O":
        explain_ai2(board, max_step, curr)
        _expected, board = min_step(board, curr)
    else:
        raise ValueError("Invalid Value for Character")
    print()
    return board


def play_game(board):
    if board.count(".") != 9:
        aifirst = True
        if board.count("X") == board.count("O"):
            curr = "X"
        else:
            curr = "O"
    else:
        _in = input("Should I be X or O? ").upper()
        if _in == "X":
            curr = "X"
            aifirst = True
        else:
            curr = "X"
            aifirst = False

    while "." in board:
        if aifirst:
            board = ai_move(board, curr)
            curr = get_player(curr)
            board = human_move(board, curr)
            curr = get_player(curr)
        else:
            board = human_move(board, curr)
            curr = get_player(curr)
            board = ai_move(board, curr)
            curr = get_player(curr)

        # check game over:
        if win := game_over2a(board):
            if win == "~DRAW":
                print("Game is a draw.")
                return
            print(f"{win} wins! 🏆")
            return

    print_board(board)


def open_indices(board):
    return [i for i, ltr in enumerate(board) if ltr == "."]

def update_board(board, ind, current_player):
    toMove = "O"
    if current_player == "O":
        toMove = "X"

        board = board[:ind] + toMove + board[ind + 1 :] # update board
    return strify(board)


def ai_move2(board, emptList, curr):
    lscores = []
    if curr == "X":
        for empty in emptList:
            new_board = strify(board[:empty] + curr + board[empty + 1 :])
            score = min_step(new_board)
            lscores.append((empty, score))

            if score == -1:
                print("Moving at " + str(empty) + " results in a loss.")
            if score == 0:
                print("Moving at " + str(empty) + " results in a tie.")
            if score == 1:
                print("Moving at " + str(empty) + " results in a win.")

        print()

        max_y = -2
        max_yidx = -1

        for x, y in lscores:
            if y > max_y:
                max_y = y
                max_yidx = x

        print("I choose space " + str(max_yidx))
        next_board = strify(board[:max_yidx] + "X" + board[max_yidx + 1 :])
        return next_board

    if curr == "O":
        for empty in emptList:
            new_board = board[:empty] + curr + board[empty + 1 :]
            score = max_step(new_board)
            lscores.append((empty, score))
            if score == -1:
                print("Moving at " + str(empty) + " results in a win.")
            if score == 0:
                print("Moving at " + str(empty) + " results in a tie.")
            if score == 1:
                print("Moving at " + str(empty) + " results in a loss.")

        print()

        min_y = 2
        min_yidx = -1

        for x, y in lscores: # find the minimum score
            if y < min_y: 
                min_y = y # update the minimum score
                min_yidx = x # index of the minimum score

        print("I choose space " + str(min_yidx))
        next_board_2 = board[:min_yidx] + "O" + board[min_yidx + 1 :]
        return next_board_2


def main():
    curr_board = sys.argv[1] if len(sys.argv) > 1 else "........." # default board if there are no cmd args

    if curr_board.count(".") == 9:
        curr = input("Should I be X or O? ").upper()
        if curr == "X":
            playIter = 0 # use the mod to find out who goes first
        else:
            playIter = 1

    else:
        num_x = curr_board.count("X")
        num_o = curr_board.count("O")
 
        if num_x == num_o: # if the number of Xs and Os are equal, then it's X's turn
            curr = "X"
            playIter = 0
        else:
            curr = "O"
            playIter = 0

    while not game_over4(curr_board)[0]:
        print()
        print("Current board:")
        print_board(curr_board)

        list_empty = open_indices(curr_board) # get the list of empty spaces

        if playIter % 2 == 0:
            player_playing = curr
            next_board = ai_move2(curr_board, list_empty, player_playing)
            curr_board = next_board
        else:
            if curr == "X":
                player_playing = "O"
            else:
                player_playing = "X"
            print("You can move to any of these spaces: " + str(list_empty) + ".")
            spaceMove = int(input(f"Which space do you want to put a {player_playing} on: "))
            while spaceMove not in list_empty:
                spaceMove = int(input(f"Which space do you want to put a {player_playing} on??? ")) # make sure the user enters a valid space
            next_board = update_board(curr_board, spaceMove, curr)
            curr_board = next_board

        playIter += 1

    print("")

    print("Current board:")
    print_board(curr_board)

    _es, result = game_over4(curr_board) 

    if result == 0:
        print("Game is a draw.")

    elif result == 1:
        if curr == "X":
            print("I win! 🏆") 
        else:
            print("You win! 🏆")
    else:
        if curr == "X":
            print("You win! 🏆")
        else:
            print("I win! 🏆")


if __name__ == "__main__":
    main()
