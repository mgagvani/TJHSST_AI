import sys
import heapq
from collections import deque
from time import perf_counter

def swap(cubestate, boardstate, idx, movement):
    c = list(cubestate)
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
    return newcubestate, newboardstate, idx


def getChildren(case, cubestate):
    size = int(case[0])
    numsquares = size ** 2
    children = [] # child structure ("board state", "cube state") TOP BOTTOM LEFT RIGHT FRONT BACK
    cubeidx = int(case[2])
    boardstate = case[1] 
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
        for child in getChildren(case, v[1]):
            print(child)
            if child not in visited:
                newNode = (child[1], child[0], child[2])
                fringe.append((newNode, _l + 1)) # ADD ONE TO PARENT"S LEVEL
                visited.add(newNode)
    return -1
    

if __name__ == "__main__":
    file = sys.argv[1]
    with open(file) as f:
        cases = [line.strip().split(" ") for line in f]

    for i, case in enumerate(cases):
        print(bfs(case))



"""
TOP BOTTOM LEFT RIGHT FRONT BACK (0 1 2 3 4 5)

flip up: (new arrangement)

BACK FRONT LEFT RIGHT BOTTOM TOP (5 4 2 3 1 0)

flip down:

FRONT BACK LEFT RIGHT BOTTOM TOP (4 5 2 3 1 0)

flip left:

RIGHT LEFT TOP BOTTOM FRONT BACK (3 2 0 1 4 5)

flip right:

LEFT RIGHT BOTTOM TOP FRONT BACK (2 3 1 0 4 5)
"""