import sys
import time
from collections import deque

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

def kDFS(start, goal, size, k):
    fringe = deque()
    start_node = (start, 0, set()) # 0-string, 1-depth, 2-ancestors
    start_node[2].add(start)
    fringe.append(start_node)
    while len(fringe) > 0:
        v = fringe.pop() # stack, not queue
        if v[0] == goal:
            return v
        if v[1] < k:
            for child in get_children(v[0], size):
                if child not in v[2]:
                    ancestors = set(v[2])
                    ancestors.add(c)
                    fringe.append((child, v[1]+1, ancestors))
    return None

def ID_DFS(start, goal, size):
    max_depth = 0
    result = None
    while result is None:
        result = kDFS(start, goal, size, max_depth)
        max_depth += 1
    return result


if __name__ == "__main__":
    args = sys.argv
    path = args[1]
    
    with open(path) as fileReader:
        line_list = [line.strip() for line in fileReader]

    for i, line in enumerate(line_list):
        a = time.perf_counter()

        size, start = load_string(line)
        goal = find_goal(start)
        b = time.perf_counter()

        _found, level = bfs(start, goal, size)
        ba = time.perf_counter()
        level = ID_DFS(start, goal, size) [1]
        bb = time.perf_counter()

        c = time.perf_counter()
        print(f"[BFS]    Line {i}: {to_str(start)}, {level} moves found in {ba-b} seconds")
        print(f"[ID-DFS] Line {i}: {to_str(start)}, {level} moves found in {bb - ba} seconds")
