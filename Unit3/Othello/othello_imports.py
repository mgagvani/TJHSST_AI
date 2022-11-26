# Othello Imports
# Manav Gagvani

EMPTY = "."
WIDTH = 8
HEIGHT = 8
assert WIDTH == HEIGHT

# copied from slider puzzles
def to_mat2(s, n):
    return list(map(list, zip(*[map(str, s)] * n)))

def isOnBoard(x, y):			
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1

def isValidMove(board, tile, xstart, ystart):		
    # Returns False if the player's move on space xstart, ystart is invalid.		
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.		
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):		
        return False		
		
    if tile == 'x':		
        otherTile = 'o'		
    else:		
        otherTile = 'x'		
		
    tilesToFlip = []		
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:		
        x, y = xstart, ystart		
        x += xdirection # First step in the x direction		
        y += ydirection # First step in the y direction		
        while isOnBoard(x, y) and board[x][y] == otherTile:		
            # Keep moving in this x & y direction.		
            x += xdirection		
            y += ydirection		
            if isOnBoard(x, y) and board[x][y] == tile:		
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.		
                while True:		
                    x -= xdirection		
                    y -= ydirection		
                    if x == xstart and y == ystart:		
                        break		
                    tilesToFlip.append([x, y])		
		
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.		
        return -1		
    return tilesToFlip

def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    mat = to_mat2(board, HEIGHT)
    validMoves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(mat, tile, x, y) != -1:
                validMoves.append(y * HEIGHT + x)
    return validMoves

def possible_moves(board, token):
    return set(getValidMoves(board, token))


def possible_moves0(board, token):
    """
    accepts a 64 char string and a single character (either x or o)
    """
    opponent = "xo"["ox".index(token)]
    directions = [-11, -10, -9, -1, 1, 9, 10, 11]
    moves = []
    for idx, tk in enumerate(board):
        if tk == opponent:
            for dir in directions:
                new = board[idx + dir] if -1 < idx + dir < 64 else 100
                if new == 100:
                    continue
                opposite = board[idx - dir] if -1 < idx - dir < 64 else 100
                if new == 100:
                    continue
                if new == EMPTY and opposite == token:
                    moves.append(idx + dir)
                elif opposite == token:
                    visited = []
                    newIdx = idx + dir * 2 if -1 < idx + dir * 2 < 64 else 100
                    if newIdx == 100:
                        continue
                    visited.append(newIdx)
                    while -1 < newIdx < 64 and board[newIdx] == tk:
                        newIdx += dir
                        visited.append(newIdx)
                    moves.append(newIdx)
                else:
                    pass # do not process pieces in the middle of a chain
    return set([int(a) for a in moves])

def make_move(board, token, index):
    pass
