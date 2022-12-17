# Othello Imports
# Manav Gagvani
import sys


EMPTY = "."
WIDTH = 8
HEIGHT = 8
assert WIDTH == HEIGHT

# copied from slider puzzles
def to_mat2(s, n):
    return list(map(list, zip(*[map(str, s)] * n)))


def eight2ten_board(board):
    # mat = to_mat2(board, 8)
    # mat.append(0, list("??????????"))
    # for row in mat:
    #     row.append(0, "?")
    #     row.append("?")
    # mat.append(list("??????????"))
    finalString = "??????????"
    for x in range(8):
        finalString += "?" + board[x * 8 : x * 8 + 8] + "?"
    finalString += "??????????"
    return finalString


def ten2eight_board(board):
    return board.replace("?", "")


def tenidx2eightidx(idx):
    return (idx // 10 - 1) * 8 + idx % 10 - 1


def possible_moves(bord, token):
    board = eight2ten_board(bord)
    moves = []
    directions = [-11, -10, -9, -1, 1, 9, 10, 11]
    opponent = "xo"["ox".index(token)]
    for idx, tk in enumerate(board):
        if tk == opponent:
            for dir in directions:
                newSpot = board[idx + dir]
                opposite = board[idx - dir]
                if newSpot == EMPTY and opposite == token:
                    moves.append(tenidx2eightidx(idx + dir))
                elif opposite == token and newSpot == opponent:
                    newIdx = idx + (dir * 2)
                    while board[newIdx] == opponent:
                        newIdx += dir
                    if board[newIdx] == EMPTY:
                        moves.append(tenidx2eightidx(newIdx))
    return list(set(moves))
    # """
    # accepts a 100 char string and a single character (either x or o)
    # """
    # opponent = "xo"["ox".index(token)]
    # directions = [-11, -10, -9, -1, 1, 9, 10, 11]
    # moves = []
    # board = eight2ten_board(bord)
    # for idx, tk in enumerate(board):
    #     if tk == opponent:
    #         for dir in directions:
    #             new = board[idx + dir] if 10 < idx + dir < 74 else 100
    #             if new == 100:
    #                 continue
    #             opposite = board[idx - dir] if 10 < idx - dir < 74 else 100
    #             if new == 100:
    #                 continue
    #             if new == EMPTY and opposite == token:
    #                 print(f"trigger one {idx + dir} {idx - dir} {idx} {dir}")
    #                 moves.append(idx + dir)
    #             elif opposite == token:
    #                 visited = []
    #                 newIdx = idx + dir * 2 if 10 < idx + dir * 2 < 74 else 100
    #                 if newIdx == 100:
    #                     continue
    #                 visited.append(newIdx)
    #                 while 10 < newIdx < 74 and board[newIdx] == tk:
    #                     newIdx += dir
    #                     visited.append(newIdx)
    #                 print(f"trigger chain {newIdx} {idx - dir} {idx} {dir}")
    #                 moves.append(newIdx)
    #             else:
    #                 pass # do not process pieces in the middle of a chain
    # return set([tenidx2eightidx(int(a)) for a in moves])


def valid10(idx):
    return -1 < tenidx2eightidx(idx) < 100


def valid8(idx):
    return -1 < idx < 64


'''
def make_move(board, token, index):
    """
    accepts a 64 char string, a single character (either x or o), and an integer
    """
    # board = list(eight2ten_board(board))
    board = list(board)
    opponent = "xo"["ox".index(token)]
    # directions = [-11, -10, -9, -1, 1, 9, 10, 11]
    directions = [-9, -8, -7, -1, 1, 7, 8, 9]
    for dir in directions:
        # newIdx = index + dir
        # if not valid8(newIdx):
        #     continue
        visited = [index]
        newIdx=index+dir
        while valid8(newIdx) and board[newIdx] == opponent:
            print(newIdx)
            visited.append(newIdx)
            newIdx += dir
        if valid8(newIdx) and board[newIdx] == token:
            for idx in visited:
                print(idx, board[idx])
                board[idx] = token


    return "".join(board)
'''


def make_move(board, token, index):
    board = board[:index] + token + board[index + 1 :]

    matrix = to_mat2(board, 8)
    i = int(index / 8)
    j = int(index % 8)

    test_i = i
    test_j = j
    test_cons = 0

    # up

    while test_i > 0:
        test_i = test_i - 1
        elem = matrix[test_i][test_j]

        if elem == EMPTY or (elem == token and test_cons == 0):
            break

        else:
            test_cons = test_cons + 1

            if elem == token:
                test_i_2 = test_i + 1
                elem_2 = matrix[test_i_2][test_j]

                while elem_2 != token:
                    matrix[test_i_2][test_j] = token
                    test_i_2 = test_i_2 + 1
                    elem_2 = matrix[test_i_2][test_j]

                break

    test_i = i
    test_j = j
    test_cons = 0

    # down

    while test_i < 7:
        test_i = test_i + 1
        elem = matrix[test_i][test_j]

        if elem == EMPTY or (elem == token and test_cons == 0):
            break

        else:
            test_cons = test_cons + 1

            if elem == token:
                test_i_2 = test_i - 1
                elem_2 = matrix[test_i_2][test_j]

                while elem_2 != token:
                    matrix[test_i_2][test_j] = token
                    test_i_2 = test_i_2 - 1
                    elem_2 = matrix[test_i_2][test_j]

                break

    test_i = i
    test_j = j
    test_cons = 0

    # left

    while test_j > 0:
        test_j = test_j - 1
        elem = matrix[test_i][test_j]

        if elem == EMPTY or (elem == token and test_cons == 0):
            break

        else:
            test_cons = test_cons + 1

            if elem == token:
                test_j_2 = test_j + 1
                elem_2 = matrix[test_i][test_j_2]

                while elem_2 != token:
                    matrix[test_i][test_j_2] = token
                    test_j_2 = test_j_2 + 1
                    elem_2 = matrix[test_i][test_j_2]

                break

    test_i = i
    test_j = j
    test_cons = 0

    # right

    while test_j < 7:
        test_j = test_j + 1
        elem = matrix[test_i][test_j]

        if elem == EMPTY or (elem == token and test_cons == 0):
            break

        else:
            test_cons = test_cons + 1

            if elem == token:
                test_j_2 = test_j - 1
                elem_2 = matrix[test_i][test_j_2]

                while elem_2 != token:
                    matrix[test_i][test_j_2] = token
                    test_j_2 = test_j_2 - 1
                    elem_2 = matrix[test_i][test_j_2]

                break

    test_i = i
    test_j = j
    test_cons = 0

    # up-left

    while test_i > 0 and test_j > 0:
        test_i = test_i - 1
        test_j = test_j - 1
        elem = matrix[test_i][test_j]

        if elem == EMPTY or (elem == token and test_cons == 0):
            break

        else:
            test_cons = test_cons + 1

            if elem == token:
                test_i_2 = test_i + 1
                test_j_2 = test_j + 1
                elem_2 = matrix[test_i_2][test_j_2]

                while elem_2 != token:
                    matrix[test_i_2][test_j_2] = token
                    test_i_2 = test_i_2 + 1
                    test_j_2 = test_j_2 + 1
                    elem_2 = matrix[test_i_2][test_j_2]

                break

    test_i = i
    test_j = j
    test_cons = 0

    # down-right

    while test_i < 7 and test_j < 7:
        test_i = test_i + 1
        test_j = test_j + 1
        elem = matrix[test_i][test_j]

        if elem == EMPTY or (elem == token and test_cons == 0):
            break

        else:
            test_cons = test_cons + 1

            if elem == token:
                test_i_2 = test_i - 1
                test_j_2 = test_j - 1
                elem_2 = matrix[test_i_2][test_j_2]

                while elem_2 != token:
                    matrix[test_i_2][test_j_2] = token
                    test_i_2 = test_i_2 - 1
                    test_j_2 = test_j_2 - 1
                    elem_2 = matrix[test_i_2][test_j_2]

                break

    test_i = i
    test_j = j
    test_cons = 0

    # up-right

    while test_i > 0 and test_j < 7:
        test_i = test_i - 1
        test_j = test_j + 1
        elem = matrix[test_i][test_j]

        if elem == EMPTY or (elem == token and test_cons == 0):
            break

        else:
            test_cons = test_cons + 1

            if elem == token:
                test_i_2 = test_i + 1
                test_j_2 = test_j - 1
                elem_2 = matrix[test_i_2][test_j_2]

                while elem_2 != token:
                    matrix[test_i_2][test_j_2] = token
                    test_i_2 = test_i_2 + 1
                    test_j_2 = test_j_2 - 1
                    elem_2 = matrix[test_i_2][test_j_2]

                break

    test_i = i
    test_j = j
    test_cons = 0

    # down-left

    while test_i < 7 and test_j > 0:
        test_i = test_i + 1
        test_j = test_j - 1
        elem = matrix[test_i][test_j]

        if elem == EMPTY or (elem == token and test_cons == 0):
            break

        else:
            test_cons = test_cons + 1

            if elem == token:
                test_i_2 = test_i - 1
                test_j_2 = test_j + 1
                elem_2 = matrix[test_i_2][test_j_2]

                while elem_2 != token:
                    matrix[test_i_2][test_j_2] = token
                    test_i_2 = test_i_2 - 1
                    test_j_2 = test_j_2 + 1
                    elem_2 = matrix[test_i_2][test_j_2]

                break

    board_2 = ""

    for k in range(8):
        for l in range(8):
            board_2 += matrix[k][l]

    return board_2


def score(board):
    '''
    # to win against random, emphasize mobility in early stages
    # and number of tokens gained in later stages
    # currently is not good - we should apply these principles to the new one
    if board.count(EMPTY) == 0: # if the board is full
        score = (((board.count("x") - board.count("o"))) * 99999999999999999999999999)  # return a very high score
        return score
    if board.count(EMPTY) > 32:
        score = ((board.count("x") - board.count("o")) * 1)
        score += sum((len(possible_moves(board, "x")), len(possible_moves(board, "o")))) * 10
        return score
    else:  # value tokens gained
        score = ((board.count("x") - board.count("o")) * 10)
        return score
    '''
    if board.count(EMPTY) == 0: # if the board is full
        score = (((board.count("x") - board.count("o"))) * 99999999999999999999999999)  # return a very high score 
        return score

    score = 0
    corner = [0, 0, 0, 7, 7, 7, 56, 56, 56, 63, 63, 63]
    next_to_corner = {1, 8, 9, 6, 14, 15, 48, 49, 57, 54, 55, 62} # set introduces some randomness?? nvm
    edge = [2, 3, 4, 5, 16, 24, 32, 40, 58, 59, 60, 61, 23, 31, 39, 47]
    two_away = {16, 23, 40, 47} 

    empty = board.count(EMPTY)
    xcount = board.count("x")
    ocount = board.count("o")
    if empty > 32: 
        score += sum((len(possible_moves(board, "x")), len(possible_moves(board, "o")))) * 5000 * (64 - empty) # value more if there are more empty squares
    # elif empty < 8: # prioritize having more pieces than the opponent in the endgame
    if xcount > ocount:
        proportion = board.count("x") / board.count("o")
        # print("score impact: ", 10 ** (int(proportion)), proportion)
        score += 20 ** (int(proportion))
    elif ocount > xcount:
        proportion = board.count("o") / board.count("x")
        # print("score impact: ", 10 ** (int(proportion)), proportion)
        score -= 20 ** (int(proportion))
    else:
        pass # score does not change if they are tied

    for corn in corner: # value corners a lot
        if(board[corn] == 'o'):
            score -= 1000000
        elif(board[corn] == 'x'):
            score += 1000000
    
    for num in two_away: 
        if(board[num] == 'x'):
            score += 40000
        elif(board[num] == 'o'):
            score -= 40000

    for edge in edge: # value edges more
        if(board[edge] == 'o'): 
            score -= 60000
        elif(board[edge] == 'x'):
            score += 60000

    for next_corn, corn_check in zip(next_to_corner, corner): # this is basically a dictionary
        if(board[next_corn] == 'x' and board[corn_check] == EMPTY): # if the next to corner is x and the corner is empty
            score -= 275000
        elif(board[next_corn] == 'x' and board[corn_check] == 'x'):
            score += 275000
        elif(board[next_corn] == 'o' and board[corn_check] == EMPTY):
            score += 275000
        elif(board[next_corn] == 'o' and board[corn_check] == 'o'): # if the next to corner is o and the corner is also o
            score -= 275000

    for i in range(0, 56, 7): # check for 2 in a row
        string_check = board[i:i + 8]

        if(string_check.count('x') >= 7):
            score += 100000
        elif(string_check.count('o') >= 7):
            score -= 100000
    
    for i in range(0, 8): # check 2nd
        string_check = board[i:64:8] 

        if(string_check.count('x') >= 7):
            score += 100000
        elif(string_check.count('o') >= 7):
            score -= 100000

    diag_1 = board[0:64:9] 
    diag_2 = board[7:57:7] 

    if(diag_1.count('x') >= 7):
        score += 100000
    elif(diag_1.count('o') >= 7):
        score -= 100000
    
    if(diag_2.count('x') >= 7):
        score += 100000 
    elif(diag_2.count('o') >= 7):
        score -= 100000

    poss_to_move = len(possible_moves(board, 'x')) # value the number of possible moves
    poss_to_move_2 = len(possible_moves(board, 'o'))

    score += (poss_to_move - poss_to_move_2) * 10000 * empty # value more if there are more possible moves (mobility)
    return score
    '''
    
    if board.count(EMPTY) == 0:
        return (board.count("x") - board.count("o")) * 100000000000
    # return board.count("x") - board.count("o")    
    score = 0
    empty = board.count(EMPTY)

    # mobility
    if empty > 32:
        score += sum((len(possible_moves(board, "x")), len(possible_moves(board, "o")))) * 5 * (64 - empty) # value more if there are more empty squares
    # corners
    for p in {0, 7, 56, 63}:
        if board[p] == 'x':
            score += 10000
        if board[p] == 'o':
            score -= 10000
    # corner adjacents (reversed)
    corners_dict = {
    0: {1, 8, 9},
    7: {6, 14, 15},
    56: {57, 48, 49},
    63: {62, 54, 55}
    }
    for x, y in corners_dict.items():
        if board[x] == EMPTY:
            for z in y:
                if board[z] == 'x':
                    score -= 200
                if board[z] == 'o':
                    score += 200
    # edges
    for p in {1, 2, 3, 4, 5, 6, 8, 16, 24, 32, 40, 48, 9, 17, 25, 33, 41, 49, 57, 10, 18, 26, 34, 42, 50, 58, 11, 19, 27, 35, 43, 51, 59, 12, 20, 28, 36, 44, 52, 60, 13, 21, 29, 37, 45, 53, 61, 14, 22, 30, 38, 46, 54, 62, 15, 23, 31, 39, 47, 55, 63}: 
        if board[p] == 'x':
            score += 10
        if board[p] == 'o':
            score -= 10
    # num pieces
    score += board.count("x") - board.count("o")
    return score
    '''



def game_over(board):
    moves = (len(possible_moves(board, "x")), len(possible_moves(board, "o")))
    # if sum(moves) == 0:
    #     return True
    # return False
    return not sum(moves)


def minimax0(board, current_player, depth, a, b):
    if (
        depth == 0 # end of iterating
        or game_over(board) 
        or len(possible_moves(board, current_player)) == 0 # no moves available
    ):
        return score(board)

    available_indices = possible_moves(board, current_player)

    if current_player == "x":
        value = float("-inf")
        for idx in available_indices:
            new_board = make_move(board, "x", idx)
            value = max(value, minimax(new_board, "o", depth - 1, a, b))
            # "ALPHA/BETA PRUNING HERE"
            a = max(a, value)

            if value >= b:
                break

        return value

    elif current_player == "o":
        value = float("inf")
        for idx in available_indices:
            new_board = make_move(board, "o", idx)
            value = min(value, minimax(new_board, "x", depth - 1, a, b))

            b = min(b, value)

            if value <= a:
                break

        return value
    
    else:
        return ValueError("current_player must be x or o")

def minimax(board, current_player, depth, a, b):
    if (
        depth == 0 # end of iterating
        or game_over(board) 
        or len(possible_moves(board, current_player)) == 0 # no moves available
    ):
        return score(board)

    available_indices = possible_moves(board, current_player)

    if current_player == "x":
        value = float("-inf")
        for idx in available_indices:
            new_board = make_move(board, "x", idx)

            # Negascout search logic:
            if value == a:
                value = max(value, minimax(new_board, "o", depth - 1, value, value + 1))
            else:
                value = max(value, minimax(new_board, "o", depth - 1, a, b))

            # Update alpha and beta values:
            a = max(a, value)
            # b = min(b, value)

        return value

    elif current_player == "o":
        value = float("inf")
        for idx in available_indices:
            new_board = make_move(board, "o", idx)

            # Negascout search logic:
            if value == b:
                value = min(value, minimax(new_board, "x", depth - 1, value - 1, value))
            else:
                value = min(value, minimax(new_board, "x", depth - 1, a, b))

            # Update alpha and beta values:
            # a = max(a, value)
            b = min(b, value)

        return value
    
    


def find_next_move(board, player, depth):
    moves = []
    a = float("-inf") # python trick for big number
    b = float("inf") # ALPHA/BETA PRUNING HERE

    if player == "x":
        moves = [
            (minimax0(make_move(board, player, i), "o", depth, a, b), i)
            for i in (possible_moves(board, player))
        ]
        print(moves)
        return max(moves, key=lambda x: x[0])[1] # lambda func rets the max value from tuple

    elif player == "o":
        moves = [
            (minimax0(make_move(board, player, i), "x", depth, a, b), i)
            for i in (possible_moves(board, player))
        ]
        print(moves)
        return min(moves, key=lambda x: x[0])[1]
    else:
        return ValueError("player must be x or o")


class Strategy:
    logging = True  # Optional

    def best_strategy(self, board, player, best_move, still_running):
        depth = 1

        for count in range(
            board.count(EMPTY)
        ):  # No need to look more spaces into the future than exist at all
            print(depth)
            best_move.value = find_next_move(board, player, depth)
            print(best_move.value)
            depth += 1


if __name__ == "__main__":
    board = sys.argv[1]

    player = sys.argv[2]

    depth = 1

    for count in range(
        board.count(EMPTY)
    ):  # No need to look more spaces into the future than exist at all

        print(find_next_move(board, player, depth))

        depth += 1
