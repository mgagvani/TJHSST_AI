import sys
import time
from collections import deque
# from itertools import permutations



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
    # mat = to_mat(str, size)
    children = []

    # mat = self.to_matrix()
    # find the dot

    # for (i, row) in enumerate(mat):
    #     for (j, val) in enumerate(row):
    #         if val == '.':
    #             di, dj = i, j
    #             break

    idx = str.find(".")

    # horizontal swapping

    # print(f"di,dj = ({di},{dj}), value is {mat[di][dj]}")
    # print(mat)

    if idx % size == 0:  # swap with right neighbour
        a = str
        ch1 = str[idx]
        ch2 = str[idx + 1]
        a = a.replace(ch2, '!',) # just a temporary
        a = a.replace(ch1, ch2)
        a = a.replace('!', ch1)
        children.append(a)
    elif (idx+1) % size == 0:
        # swap with left neighbour
        b = str
        ch1 = str[idx]
        ch2 = str[idx - 1]
        b = b.replace(ch2, '!',) # just a temporary
        b = b.replace(ch1, ch2)
        b = b.replace('!', ch1)
        children.append(b)
    else:
        # swap with both neigubours
        c = str
        ch1 = str[idx]
        ch2 = str[idx + 1]
        c = c.replace(ch2, '!',) # just a temporary
        c = c.replace(ch1, ch2)
        c = c.replace('!', ch1)
        children.append(c)
        d = str
        ch1 = str[idx]
        ch2 = str[idx - 1]
        d = d.replace(ch2, '!',) # just a temporary
        d = d.replace(ch1, ch2)
        d = d.replace('!', ch1)
        children.append(d)

    # vertical swapping
    # print(mat)

    if idx < size:  # swap with below neighbour
        e = str
        ch1 = str[idx]
        ch2 = str[idx + size]
        e = e.replace(ch2, '!',) # just a temporary
        e = e.replace(ch1, ch2)
        e = e.replace('!', ch1)
        children.append(e)
    elif idx >= size * (size - 1):
        # swap with above
        f = str
        ch1 = str[idx]
        ch2 = str[idx - size]
        f = f.replace(ch2, '!',) # just a temporary
        f = f.replace(ch1, ch2)
        f = f.replace('!', ch1)
        children.append(f)
    else:
          # swap with both neigubours
        g = str
        ch1 = str[idx]
        ch2 = str[idx + size]
        g = g.replace(ch2, '!',) # just a temporary
        g = g.replace(ch1, ch2)
        g = g.replace('!', ch1)
        children.append(g)
        h = str
        ch1 = str[idx]
        ch2 = str[idx - size]
        h = h.replace(ch2, '!',) # just a temporary
        h = h.replace(ch1, ch2)
        h = h.replace('!', ch1)
        children.append(h)
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

def modBFS2(start): 
    fringe = deque()
    visited = set()
    fringe.append((start, 0))
    visited.add(start)
    counter = 0
    allv = []
    while len(fringe) > 0:
        v, _l = fringe.popleft() # DIS IS PARENT
        if _l == 31:
            counter += 1
            allv.append(v)
            continue
        for child in get_children(v, 3):
            if child not in visited:
                fringe.append((child, _l + 1)) # ADD ONE TO PARENT"S LEVEL
                visited.add(child)
    return counter, allv

    


# def generate_puzzles(size):
#     sizey = size * size
#     s = ""
#     for i in range(sizey - 1):
#         s += chr(i + 65)
#     s += "."
#     perms = [''.join(p) for p in permutations(list(s))]
#     return perms

# ANSWERS TO QUESTIONS:
"""
1. 181452
2. ABCDEFHG. because you cannot swap the H and G without moving the rest.
3. 286
4. 8672543.1 and 64785.321 both have a path length of 31
5. 22 steps takes 59 seconds
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

    print(modBFS2("12345678.")[0])

    print(modBFS2("12345678."))
    

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
    
        

