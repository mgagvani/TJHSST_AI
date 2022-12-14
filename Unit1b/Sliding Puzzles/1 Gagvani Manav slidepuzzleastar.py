import sys
import time
from heapq import heappush, heappop, heapify
from collections import deque

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

def to_mat2(s, n):
    return list(map(list, zip(*[map(str, s)] * n)))

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

def incremental_taxicab(ch1, ch2, goal_positions, idx, idxnew, curr_taxicab, size):
    _abs = abs
    inc_taxicab = curr_taxicab
    (gx, gy) = goal_positions[ch1]
    (x, y) = (idx // size, idx % size)
    inc_taxicab -= _abs(gx - x) + _abs(gy - y)
    (x, y) = (idx // size, (idxnew) % size)
    inc_taxicab += _abs(gx - x) + _abs(gy - y)

    (gx, gy) = goal_positions[ch2]
    (x, y) = (idx // size, idx % size)
    inc_taxicab -= _abs(gx - x) + _abs(gy - y)
    (x, y) = (idx // size, (idxnew) % size)
    inc_taxicab += _abs(gx - x) + _abs(gy - y)
    return inc_taxicab
    
# given parent and taxicab of parent, compute children and taxicab of children incrementaly
def increment_children(str, size, curr_taxicab, goal_positions):
    children = []
    idx = str.find(".")
    ch1 = str[idx]

    # horizontal swapping
    if idx % size == 0:  # swap with right neighbour
        a = str
        ch2 = str[idx + 1]
        a = a.replace(ch2, '!',) # just a temporary
        a = a.replace(ch1, ch2)
        a = a.replace('!', ch1)
        new_taxicab = incremental_taxicab(ch1, ch2, goal_positions, idx, idx + 1, curr_taxicab, size)
        children.append((a, new_taxicab))
    elif (idx+1) % size == 0:
        # swap with left neighbour
        b = str
        ch2 = str[idx - 1]
        b = b.replace(ch2, '!',) # just a temporary
        b = b.replace(ch1, ch2)
        b = b.replace('!', ch1)
        new_taxicab = incremental_taxicab(ch1, ch2, goal_positions, idx, idx - 1, curr_taxicab, size)
        children.append((b, new_taxicab))
    else:
        # swap with both neigubours
        c = str
        ch2 = str[idx + 1]
        c = c.replace(ch2, '!',) # just a temporary
        c = c.replace(ch1, ch2)
        c = c.replace('!', ch1)
        new_taxicab = incremental_taxicab(ch1, ch2, goal_positions, idx, idx + 1, curr_taxicab, size)
        children.append((c, new_taxicab))
        d = str
        ch2 = str[idx - 1]
        d = d.replace(ch2, '!',) # just a temporary
        d = d.replace(ch1, ch2)
        d = d.replace('!', ch1)
        new_taxicab = incremental_taxicab(ch1, ch2, goal_positions, idx, idx - 1, curr_taxicab, size)
        children.append((d, new_taxicab))

    # vertical swapping
    if idx < size:  # swap with below neighbour
        e = str
        ch2 = str[idx + size]
        e = e.replace(ch2, '!',) # just a temporary
        e = e.replace(ch1, ch2)
        e = e.replace('!', ch1)
        new_taxicab = incremental_taxicab(ch1, ch2, goal_positions, idx, idx + size, curr_taxicab, size)
        children.append((e, new_taxicab))
    elif idx >= size * (size - 1):
        # swap with above
        f = str
        ch2 = str[idx - size]
        f = f.replace(ch2, '!',) # just a temporary
        f = f.replace(ch1, ch2)
        f = f.replace('!', ch1)
        new_taxicab = incremental_taxicab(ch1, ch2, goal_positions, idx, idx - size, curr_taxicab, size)
        children.append((f, new_taxicab))
    else:
          # swap with both neigubours
        g = str
        ch2 = str[idx + size]
        g = g.replace(ch2, '!',) # just a temporary
        g = g.replace(ch1, ch2)
        g = g.replace('!', ch1)
        new_taxicab = incremental_taxicab(ch1, ch2, goal_positions, idx, idx + size, curr_taxicab, size)
        children.append((g, new_taxicab))
        h = str
        ch2 = str[idx - size]
        h = h.replace(ch2, '!',) # just a temporary
        h = h.replace(ch1, ch2)
        h = h.replace('!', ch1)
        new_taxicab = incremental_taxicab(ch1, ch2, goal_positions, idx, idx - size, curr_taxicab, size)
        children.append((h, new_taxicab))
    return children

    

# def get_children(str, size, curr_taxicab, goal_positions):
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
        # TODO add incremental taxicab calculation
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
    return total, goal_positions


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

def taxicab_new(current, goal_positions, size):
    currmat = to_mat2(current, size)
    total = 0

    for (i, row) in enumerate(currmat):
        for (j, val) in enumerate(row):
            if val == ".":
                continue # SKIP THE DOT
            goali, goalj = goal_positions[val]
            dy, dx = abs(goali - i), abs(goalj - j)
            total += (dy + dx)
    return total

def taxicab_new2(current, goal_positions, size):
    total = 0
    for a, val in enumerate(current):
        if val == ".": continue
        j = a%size; i = (a-j)//4
        goali, goalj = goal_positions[val]
        dy, dx = abs(goali - i), abs(goalj - j)
        total += (dy + dx)
    return total

# not any faster
def incremental_astar(start, goal, size):
    # calculate initial taxicab
    initial, goal_positions = taxicab(start, goal, size)
    # A-Star
    closed = set()
    start_node = (initial, start, 0) # this tuple structure is a "node"
    fringe = [] # heap
    heappush(fringe, start_node)
    while len(fringe) > 0:
        v = heappop(fringe)
        if v[1] == goal:
            return v # well something more will come here later
        if v[1] not in closed:
            closed.add(v[1])
            for child, new_taxicab in increment_children(v[1], size, [taxicab_new2(v[1], goal_positions, size)], goal_positions):
                if child not in closed:
                    # print(normalize(v[2], v[0]))
                    temp = (v[2]+1+new_taxicab,child, v[2]+1)
                    heappush(fringe, temp)
    return -1

def normalize(g, f):
    if g < 5:
        return 1
    return 1.25

def new_astar(start, goal, size):
    # calculate initial taxicab
    initial, goal_positions = taxicab(start, goal, size)
    # A-Star
    closed = set()
    start_node = (initial, start, 0) # this tuple structure is a "node"
    fringe = [] # heap
    heappush(fringe, start_node)
    while len(fringe) > 0:
        v = heappop(fringe)
        if v[1] == goal:
            return v # well something more will come here later
        if v[1] not in closed:
            closed.add(v[1])
            for child in get_children(v[1], size):
                if child not in closed:
                    # print(normalize(v[2], v[0]))
                    temp = (v[2]+1+taxicab_new2(child, goal_positions, size)*normalize(v[2], v[0]),child, v[2]+1)
                    heappush(fringe, temp)
    return -1

def id_astar(start, goal, size):
    bound = taxicab(start, goal, size)[0]
    path = [start]
    while True:
        t = search(path, 0, bound, size, goal)
        if t == "found":
            return bound, goal
        if t == float("inf"):
            return "n/a", goal
        # print(t)
        bound = t

def search(path, g, bound ,size, goal):
    node = path[-1]
    f = g + taxicab(node, goal, size)[0]
    if f > bound:
        return f
    if node == goal:
        return "found"
    min = float("inf")
    for child in get_children(node, size):
        if child not in path:
            path.append(child)
            t = search(path, g+taxicab(child, goal, size)[0]+1, bound, size, goal)
            if t == "found":
                return "found"
            # print(t, min)
            if t < min:
                min = t
            path.pop()
    return min

# NOTE: not working
def bi_astar(start, goal, size):
    initcost, goal_positions = taxicab(start, goal, size)
    frontier = [[], []]
    start_node1 = (initcost, start, 0)
    start_node2 = (initcost, goal, 0)
    heappush(frontier[0], start_node1)
    heappush(frontier[1], start_node2)
    sets = [{start}, {goal}]
    usestartorgoal = [start, goal]
    explored = [{start : (0, [start])}, {goal : (0, [goal])}]
    alternate = 1
    while len(frontier[0]) > 0 and len(frontier[1]) > 0:
        alternate = 1 - alternate
        v = heappop(frontier[alternate])
        sets[alternate] = sets[alternate] - {v}
        if v in sets[1 - alternate]:
            return v
        for child in get_children(v[1], size):
            if child not in explored[alternate]:
                f = taxicab(child, usestartorgoal[1 - alternate], size)[0]
                print(type(v[2]), type(f))
                heappush(frontier[alternate], (v[2]+1+f, child, v[2]+1))
                sets[alternate].add(child)
                explored[alternate][child] = (v[2]+1+f, explored[alternate][v][1])

if __name__ == "__main__":
    args = sys.argv
    path = args[1]
    if "korf100" in path:
        korfformat = True
    else:
        korfformat = False

    time0 = time.perf_counter()
    with open(path) as fileReader:
        line_list = [line.strip() for line in fileReader]

    for i, line in enumerate(line_list):
        size, start = load_string(line)
        a = time.perf_counter()

        if korfformat:
            goal = ".ABCDEFGHIJKLMNO"
            _info = incremental_astar(start, goal, size)
        else:
            goal = find_goal(start)
            if parity_check(start, size):
                _info = incremental_astar(start, goal, size)
            else:
                _info = ("no solution determined",)


        b = time.perf_counter()
    
        print(f"Line {i}: {start}, {int(_info[0])} moves in {b-a} s")
        # if i != 0:
        #     print(f"{_info[0]/i}")
        # print()
    time1 = time.perf_counter()
    print(f"Total time: {time1-time0} s")
