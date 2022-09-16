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


def swap(sourcei, sourcej, desti, destj, mat):
    # print(sourcei, sourcej, desti, destj)
    source = mat[sourcei][sourcej]
    dest = mat[desti][destj]
    # print(source, dest)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    mat[sourcei][sourcej] = dest
    mat[desti][destj] = source
    return to_str(mat)


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

    print(f"di,dj = ({di},{dj}), value is {mat[di][dj]}")

    if dj == 0:  # swap with right neighbour
        children.append(swap(di, dj, di, dj + 1, mat))
    elif dj == len(mat[0]) - 1:
        # swap with left neighbour
        children.append(swap(di, dj, di, dj - 1, mat))
    else:
          # swap with both neigubours
        children.append(swap(di, dj, di, dj + 1, mat))
        children.append(swap(di, dj, di, dj - 1, mat))

    # vertical swapping

    if di == 0:  # swap with below neighbour
        children.append(swap(di, dj, di + 1, dj, mat))
    elif di == len(mat[0]) - 1:
        # swap with above
        children.append(swap(di, dj, di - 1, dj, mat))
    else:
          # swap with both neigubours
        children.append(swap(di, dj, di + 1, dj, mat))
        children.append(swap(di, dj, di - 1, dj, mat))
    return children


def bfs(start, goal, size): # pass in strings!! (and the size of the string)
    print(matstr(to_mat(start, size)))
    print("_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_")
    fringe = deque()
    visited = set()
    fringe.append(start)
    visited.add(start)
    while len(fringe) > 0:
        v = fringe.popleft()
        if v == goal:
            return v
        for child in get_children(v, size):
            print(matstr(to_mat(child, size)))
            if child not in visited:
                fringe.append(child)
                visited.add(child)

if __name__ == "__main__":
    args = sys.argv
    path = args[1]

    with open(path) as fileReader:
        line_list = [line.strip() for line in fileReader]

    for i, line in enumerate(line_list):
        a = time.perf_counter()

        size, start = load_string(line)
        goal = find_goal(start)
        print(f"goal: {goal}")
        _found = bfs(start, goal, size)

        b = time.perf_counter()
        print(f"Line {i}: {to_str(start)},  {_found}  found in {b-a} seconds")
        break
        

