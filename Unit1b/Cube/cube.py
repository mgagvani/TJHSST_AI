import sys
from collections import deque
from time import perf_counter
from heapq import heappush, heappop, heapify

def swap(cubestate, boardstate, idx, movement):
    c = cubestate
    if movement == "up":
        newcube = c[5] + c[4] + c[3] + c[2] + c[1] + c[0]
    elif movement == "down":
        newcube = c[4] + c[5] + c[2] + c[3] + c[1] + c[0]
    elif movement == "left":
        newcube = c[3] + c[2] + c[0] + c[1] + c[4] + c[5]
    elif movement == "right":
        newcube = c[2] + c[3] + c[1] + c[0] + c[4] + c[5]
    else:
        print('INVALID MOVEMENT')

    temp = newcube[1]
    newcubestate = list(newcube)
    newcubestate[1] = boardstate[idx]
    newcubestate = "".join(newcubestate)

    newboardstate = list(boardstate)
    newboardstate[idx] = temp
    newboardstate = "".join(newboardstate)
    return newboardstate, newcubestate, idx
'''
def generateGraph():
    """
    Note: Cubestate here is in the form 012345 (string) and is agnostic of where the paint is. 
    """
    # generate all permutations of a string
    from itertools import permutations
    perms = set(["".join(p) for p in permutations("012345")])
    graph = {}
    for c in perms:
        up, down, left, right = c[5] + c[4] + c[3] + c[2] + c[1] + c[0], c[4] + c[5] + c[2] + c[3] + c[1] + c[0], c[3] + c[2] + c[0] + c[1] + c[4] + c[5], c[2] + c[3] + c[1] + c[0] + c[4] + c[5]
        graph[c] = (up, down, left, right)
    return graph

def getChildren2(boardstate, cube_occupancy, cube_arrangement, cubeidx, size, graph):
    new_arrangements = graph[cube_arrangement]
    new_occupancies = []
    for arrangement in new_arrangements:
        _a = []
        for i, str_idx in enumerate(arrangement):
            _a[int(str_idx)] = cube_occupancy[i]
        new_occupancies.append(_a)

    # transfer from board to cube, (creating new board states)
    new_boards = []
    newidxs = {0: cubeidx-size, 1: cubeidx+size, 2: cubeidx-1, 3: cubeidx+1}
    for i, occupancy in enumerate(new_occupancies):
        # up, down, left, right
        if occupancy[1] == boardstate[newidxs[i]]:
            new_boards.append(boardstate)
        else:
            # have to swap
            a = occupancy[1]
            b = boardstate[newidxs[i]]
            occupancy[1] = b
            x = list(boardstate); x[newidxs[i]] = a
            new_boards.append("".join(x))
    return list(zip(new_arrangements, new_boards, new_occupancies))
    
'''

def getChildren(boardstate, cubestate, cubeidx, size):
    # print(boardstate, cubestate, cubeidx, size)
    cubeidx = int(cubeidx)
    children = [] # child structure ("board state", "cube state") TOP BOTTOM LEFT RIGHT FRONT BACK
    # print(cubeidx, size)
    # horiz swapping
    if cubeidx % size == 0:       # swap with right neighbour
        # print("right")
        children.append(swap(cubestate, boardstate, cubeidx+1, "right"))
    elif (cubeidx+1) % size == 0: # swap with left neighbour
        # print("left")
        children.append(swap(cubestate, boardstate, cubeidx-1, "left"))
    else:                     # swap with both neigubours
        # print("right and left")
        children.append(swap(cubestate, boardstate, cubeidx+1, "right"))
        children.append(swap(cubestate, boardstate, cubeidx-1, "left"))

    # vertical swapping
    if cubeidx < size:                 # swap with below neighbour
        # print("below")
        children.append(swap(cubestate, boardstate, cubeidx+size, "down"))
    elif cubeidx >= size * (size - 1): # swap with above
        # print("above")
        children.append(swap(cubestate, boardstate, cubeidx-size, "up"))
    else:                          # swap with both neigubours
        # print("above and belwo")
        children.append(swap(cubestate, boardstate, cubeidx+size, "up"))
        children.append(swap(cubestate, boardstate, cubeidx-size, "down"))

    return children

def goaltest(cubestate):
    if cubestate == "@@@@@@":
        return True
    return False

def bfs(case): # pass in strings!! (and the size of the string)
    startNode = (case[1], "......", case[2])
    fringe = deque()
    visited = set()
    fringe.append((startNode, 0))  # STATE --> (BOARDSTATE, CUBESTATE, CUBEIDX)
    visited.add(startNode)
    while len(fringe) > 0:
        v, _l = fringe.popleft() # DIS IS PARENT
        if goaltest(v[1]):
            return v, _l
        for child in getChildren(v[0], v[1], v[2], int(case[0])): # case is (size, puzzle, idx, ___)
            if child not in visited:
                newNode = (child[1], child[0], child[2])
                fringe.append((newNode, _l + 1)) # ADD ONE TO PARENT"S LEVEL
                visited.add(newNode)
    return -1

def heuristic(boardstate):
    return boardstate.count('@')

def astar(case):
    closed = set()
    start_node = (heuristic(case[1]), (case[1], "......", case[2],), 0,) # this tuple structure is a "node"
    size = int(case[0])
    fringe = [] # heap
    heapify(fringe)
    heappush(fringe, start_node)
    while len(fringe) > 0:
        v = heappop(fringe)
        if goaltest(v[1][1]):
            return v # well something more will come here later
        if v[1] not in closed:
            closed.add(v[1])
            for child in getChildren(v[1][0], v[1][1], v[1][2], size):
                if child not in closed:
                    temp = (v[2]+1+heuristic(v[1][0]),child, v[2]+1,)
                    heappush(fringe, temp)
    return -1
    

if __name__ == "__main__":
    file = sys.argv[1]
    with open(file) as f:
        cases = [line.strip().split(" ") for line in f]

    # graph = generateGraph()
    # print(graph["012345"] , graph["320145"])

    for i, case in enumerate(cases):
        a = perf_counter()
        _answer = astar(case)
        b = perf_counter()
        print(f"{_answer} in {b-a} seconds")



"""
This is the state as represented by cubestate:
TOP BOTTOM LEFT RIGHT FRONT BACK (0 1 2 3 4 5)

NEW ARRANGEMENTS:
flip up: 
BACK FRONT LEFT RIGHT BOTTOM TOP (5 4 2 3 1 0)

flip down:
FRONT BACK LEFT RIGHT BOTTOM TOP (4 5 2 3 1 0)

flip left:
RIGHT LEFT TOP BOTTOM FRONT BACK (3 2 0 1 4 5)

flip right:
LEFT RIGHT BOTTOM TOP FRONT BACK (2 3 1 0 4 5)
"""