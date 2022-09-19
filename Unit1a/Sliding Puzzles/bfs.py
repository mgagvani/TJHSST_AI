from distutils.spawn import find_executable
from re import S
import sys
import time
from collections import deque
from itertools import permutations



def load_string(line):
    size, pstr = line.split()
    size = int(size)
    return size, pstr


def to_mat(str, size):
    mat = []
    for i in range(size):
        mat.append([])
        for j in range(size):
            mat[-1].append(str[i * size + j])
    return mat


def to_str(mat):
    s = ''
    for row in mat:
        for val in row:
            s += val
    return s


def matstr(mat):
    s = ''
    for row in mat:
        for val in row:
            s += val + ' '
        s += '\n'
    return s


def find_goal(string):
    a = sorted(string)[1:]
    a.append('.')
    return ''.join(a)


def swap(sourcei, sourcej, desti, destj, mat, size):
    # newmat = to_mat(to_str(mat), size)
    # print(sourcei, sourcej, desti, destj)
    source = mat[sourcei][sourcej]
    dest = mat[desti][destj]
    # print(source, dest)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    mat[sourcei][sourcej] = dest
    mat[desti][destj] = source
    toRet =  to_str(mat)
    # swap back
    mat[sourcei][sourcej] = source
    mat[desti][destj] = dest
    return toRet
    


def get_children(str, size):
    mat = to_mat(str, size)
    children = []

    # mat = self.to_matrix()
    # find the dot

    for (i, row) in enumerate(mat):
        for (j, val) in enumerate(row):
            if val == '.':
                di, dj = i, j
                break

    # horizontal swapping

    # print(f"di,dj = ({di},{dj}), value is {mat[di][dj]}")
    # print(mat)

    if dj == 0:  # swap with right neighbour
        children.append(swap(di, dj, di, dj + 1, mat, size))
    elif dj == len(mat[0]) - 1:
        # swap with left neighbour
        children.append(swap(di, dj, di, dj - 1, mat, size))
    else:
          # swap with both neigubours
        children.append(swap(di, dj, di, dj + 1, mat, size))
        children.append(swap(di, dj, di, dj - 1, mat, size))

    # vertical swapping
    # print(mat)

    if di == 0:  # swap with below neighbour
        children.append(swap(di, dj, di + 1, dj, mat, size))
    elif di == len(mat[0]) - 1:
        # swap with above
        children.append(swap(di, dj, di - 1, dj, mat, size))
    else:
          # swap with both neigubours
        children.append(swap(di, dj, di + 1, dj, mat, size))
        children.append(swap(di, dj, di - 1, dj, mat, size))
    return children


def bfs(start, goal, size): # pass in strings!! (and the size of the string)
    fringe = deque()
    visited = set()
    fringe.append((start, 0))
    visited.add(start)
    while len(fringe) > 0:
        v, _l = fringe.popleft() # DIS IS PARENT
        if v == goal:
            return v, _l
        for child in get_children(v, size):
            # print(matstr(to_mat(child, size)))  
            if child not in visited:
                fringe.append((child, _l + 1)) # ADD ONE TO PARENT"S LEVEL
                visited.add(child)
    return -1

def modBFS(size):
    if size == 2:
        s = "123."
    else:
        s = "12345678."
    fringe = deque()
    visited = set()
    fringe.append((s, 0))
    visited.add(s)
    while len(fringe) > 0:
        v, _l = fringe.popleft() # DIS IS PARENT
        for child in get_children(v, size):
            # print(matstr(to_mat(child, size)))  
            if child not in visited:
                fringe.append((child, _l + 1)) # ADD ONE TO PARENT"S LEVEL
                visited.add(child)
    return len(visited)

def modBFS2(start, goal): # pass in strings!! (and the size of the string)
    fringe = deque()
    visited = set()
    fringe.append((start, 0))
    visited.add(start)
    while len(fringe) > 0:
        v, _l = fringe.popleft() # DIS IS PARENT
        if v == goal and _l == 10:
            return 1
        elif _l > 10:
            return 0
        elif v == goal and _l < 10:
            return 0
        for child in get_children(v, 3):
            # print(matstr(to_mat(child, size)))  
            if child not in visited:
                fringe.append((child, _l + 1)) # ADD ONE TO PARENT"S LEVEL
                visited.add(child)
    return 0

    


def generate_puzzles(size):
    sizey = size * size
    s = ""
    for i in range(sizey - 1):
        s += chr(i + 65)
    s += "."
    perms = [''.join(p) for p in permutations(list(s))]
    return perms

# ANSWERS TO QUESTIONS:
"""
1. 181452
2. ABCDEFHG. because you cannot swap the H and G without moving the rest. 
5. 20 steps takes 47 seconds
"""

if __name__ == "__main__":
    args = sys.argv
    path = args[1]

    """
    print(modBFS(2) + modBFS(3))

    puzzles = generate_puzzles(3) 

    for puzzle in puzzles:
        goal = find_goal(puzzle)
        print(bfs(puzzle, goal, 3), puzzle, goal)
        break # delete this to find all

    a = 0
    for puzzle in puzzles:
        a += modBFS2(puzzle, "ABCDEFGH.")
        if a % 10 == 0:
            print(puzzle, a)
    print(a)
    """



    
    with open(path) as fileReader:
        line_list = [line.strip() for line in fileReader]

    for i, line in enumerate(line_list):
        a = time.perf_counter()

        size, start = load_string(line)
        goal = find_goal(start)
        # print(f"goal: {goal}")
        b = time.perf_counter()

        _found, level = bfs(start, goal, size)
        # steps = backtrack(goal, parents, start)

        c = time.perf_counter()
        print(f"Line {i}: {to_str(start)}, {level} moves found in {c-b} seconds")
    
        

