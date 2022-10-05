import sys
import time
from fibheap import *
from heapq import heappush, heappop, heapify

r"""
Run Command:
python -m cProfile -s tottime '.\1 Gagvani Manav slidepuzzleastar.py' '.\slide_puzzle_tests_2.txt'
"""

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
    source = mat[sourcei][sourcej]
    dest = mat[desti][destj]
    mat[sourcei][sourcej] = dest
    mat[desti][destj] = source
    toRet =  to_str(mat)
    # swap back
    mat[sourcei][sourcej] = source
    mat[desti][destj] = dest
    return toRet
    


def get_children(str, size):
    children = []
    idx = str.find(".")

    # horizontal swapping
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

def parity_check(string, size):
    mat = to_mat(string, size)
    for (i, row) in enumerate(mat):
        for (j, val) in enumerate(row):
            if val == '.':
                if i % 2 == 0:
                    blankEven = True
                else:
                    blankEven = False
                break

    # step 2, find even or odd parity
    numParity = 0
    newstring = string.replace(".", "")

    for i in range(len(newstring)):
        for j in range(i+1, len(newstring)):
            if ord(newstring[i]) > ord(newstring[j]):
                numParity += 1
    
    # ODD SIZE BOARDS:
    if size % 2 == 1:
        if numParity % 2 == 0:
            return True
        else:   
            return False
    else: # EVEN SIZE BOARDS
        if blankEven and numParity % 2 == 1:
            return True
        if not blankEven and numParity % 2 == 0:
            return True
        return False
            
def taxicab(current, goal, size):
    currmat = to_mat(current, size)
    goalmat = to_mat(goal, size)
    total = 0

    goal_positions = {}
    for (i, row) in enumerate(goalmat):
        for (j, val) in enumerate(row):
            goal_positions[val] = (i,j)
    
    for (i, row) in enumerate(currmat):
        for (j, val) in enumerate(row):
            if val == ".":
                continue # SKIP THE DOT
            goali, goalj = goal_positions[val]
            dy, dx = abs(goali - i), abs(goalj - j)
            total += (dy + dx)
    return total

def astar(start, goal, size):
    closed = set()
    start_node = (taxicab(start, goal, size), start, 0) # this tuple structure is a "node"
    fringe = [] # heap
    heapify(fringe)
    heappush(fringe, start_node)
    while len(fringe) > 0:
        v = heappop(fringe)
        if v[1] == goal:
            return v # well something more will come here later
        if v[1] not in closed:
            closed.add(v[1])
            for child in get_children(v[1], size):
                if child not in closed:
                    temp = (v[2]+1+taxicab(child, goal, size),child, v[2]+1)
                    heappush(fringe, temp)
    return -1

def new_astar(start, goal, size):
    closed = set()
    start_node = (taxicab(start, goal, size), start, 0) # this tuple structure is a "node"
    fringe = makefheap() # heap
    fheappush(fringe, start_node)
    while fringe.num_nodes > 0:
        v = fheappop(fringe)
        if v[1] == goal:
            return v # well something more will come here later
        if v[1] not in closed:
            closed.add(v[1])
            for child in get_children(v[1], size):
                if child not in closed:
                    temp = (v[2]+1+taxicab(child, goal, size),child, v[2]+1)
                    fheappush(fringe, temp)
    return -1

if __name__ == "__main__":
    args = sys.argv
    path = args[1]

    with open(path) as fileReader:
        line_list = [line.strip() for line in fileReader]

    for i, line in enumerate(line_list):
        size, start = load_string(line)
        a = time.perf_counter()

        if parity_check(start, size):
            _info = new_astar(start, find_goal(start), size)
        else:
            _info = ("no solution determined",)


        b = time.perf_counter()
    
        print(f"Line {i}: {start}, {_info[0]} moves in {b-a} s")
